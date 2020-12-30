import logging
from dataclasses import dataclass
from typing import Type, Any

import pika
import pinject
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.optional_component import OptionalComponent
from cato_server.mappers.internal.mapper_registry_factory import MapperRegistryFactory
from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.queues.abstract_message_queue import AbstractMessageQueue
from cato_server.queues.rabbit_mq_message_queue import RabbitMqMessageQueue
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.output_repository import OutputRepository
from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.abstract.test_heartbeat_repository import (
    TestHeartbeatRepository,
)
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import Base
from cato_server.storage.sqlalchemy.sqlalchemy_deduplicating_file_storage import (
    SqlAlchemyDeduplicatingFileStorage,
)
from cato_server.storage.sqlalchemy.sqlalchemy_image_repository import (
    SqlAlchemyImageRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_output_repository import (
    SqlAlchemyOutputRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_project_repository import (
    SqlAlchemyProjectRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_run_repository import (
    SqlAlchemyRunRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_heartbeat_repository import (
    SqlAlchemyTestHeartbeatRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)
from cato_server.usecases.create_full_run import CreateFullRunUsecase
from cato_server.usecases.fail_timed_out_tests import FailTimedOutTests
from cato_server.usecases.finish_test import FinishTest

logger = logging.getLogger(__name__)

FILE_STORAGE_IN_MEMORY = ":memory:"


@dataclass
class StorageBindings:
    project_repository_binding: Type[ProjectRepository]
    run_repository_binding: Type[RunRepository]
    suite_result_repository_binding: Type[SuiteResultRepository]
    test_result_repository_binding: Type[TestResultRepository]
    file_storage_binding: Type[AbstractFileStorage]
    output_repository_binding: Type[OutputRepository]
    image_repository: Type[ImageRepository]
    test_heartbeat_repository: Type[TestHeartbeatRepository]
    session_maker_binding: Any
    root_path_binding: str


@dataclass
class MessageQueueBindings:
    message_queue_binding: OptionalComponent[AbstractMessageQueue]


@dataclass
class Bindings:
    storage_bindings: StorageBindings
    app_configuration: AppConfiguration
    message_queue_bindings: MessageQueueBindings


class PinjectBindings(pinject.BindingSpec):
    def __init__(self, bindings: Bindings):
        self._bindings = bindings

    def configure(self, bind):
        bind(
            "project_repository",
            to_class=self._bindings.storage_bindings.project_repository_binding,
        )
        bind(
            "run_repository",
            to_class=self._bindings.storage_bindings.run_repository_binding,
        )
        bind(
            "suite_result_repository",
            to_class=self._bindings.storage_bindings.suite_result_repository_binding,
        )
        bind(
            "test_result_repository",
            to_class=self._bindings.storage_bindings.test_result_repository_binding,
        )
        bind(
            "file_storage",
            to_class=self._bindings.storage_bindings.file_storage_binding,
        )
        bind(
            "output_repository",
            to_class=self._bindings.storage_bindings.output_repository_binding,
        )
        bind(
            "image_repository",
            to_class=self._bindings.storage_bindings.image_repository,
        )
        bind(
            "test_heartbeat_repository",
            to_class=self._bindings.storage_bindings.test_heartbeat_repository,
        )
        bind("root_path", to_instance=self._bindings.storage_bindings.root_path_binding)
        bind(
            "session_maker",
            to_instance=self._bindings.storage_bindings.session_maker_binding,
        )
        bind("app_configuration", to_instance=self._bindings.app_configuration)
        bind("create_full_run_usecase", to_class=CreateFullRunUsecase)
        bind(
            "message_queue",
            to_instance=self._bindings.message_queue_bindings.message_queue_binding,
        )
        bind("fail_timed_out_tests", to_class=FailTimedOutTests)
        bind("finish_test", to_class=FinishTest)
        bind("object_mapper", to_class=ObjectMapper)
        bind(
            "mapper_registry",
            to_instance=MapperRegistryFactory().create_mapper_registry(),
        )


class BindingsFactory:
    def __init__(self, configuration: AppConfiguration):
        self._configuration = configuration

    def create_bindings(self) -> PinjectBindings:
        logger.info("Creating bindings..")
        storage_bindings = self.create_storage_bindings()
        message_queue_bindings = self.create_message_queue_bindings()
        bindings = Bindings(
            storage_bindings, self._configuration, message_queue_bindings
        )
        return PinjectBindings(bindings)

    def create_storage_bindings(self):
        logger.info("Creating storage bindings..")
        return StorageBindings(
            project_repository_binding=SqlAlchemyProjectRepository,
            run_repository_binding=SqlAlchemyRunRepository,
            suite_result_repository_binding=SqlAlchemySuiteResultRepository,
            test_result_repository_binding=SqlAlchemyTestResultRepository,
            file_storage_binding=SqlAlchemyDeduplicatingFileStorage,
            output_repository_binding=SqlAlchemyOutputRepository,
            image_repository=SqlAlchemyImageRepository,
            test_heartbeat_repository=SqlAlchemyTestHeartbeatRepository,
            root_path_binding=self._configuration.storage_configuration.file_storage_url,
            session_maker_binding=self._get_session_maker(),
        )

    def create_message_queue_bindings(self):
        logger.info("Creating message queue bindings..")
        return MessageQueueBindings(message_queue_binding=self._get_message_queue())

    def _get_session_maker(self):
        return sessionmaker(bind=self._get_engine())

    def _get_engine(self):
        database_url = self._configuration.storage_configuration.database_url
        if database_url.startswith("sqlite"):
            logger.info("Configure bindings for SQLite database..")
            engine = create_engine(database_url)
            if database_url.endswith(":memory:"):
                logger.info("SQLite in-memory detected, creating tables..")
                Base.metadata.create_all(engine)
            return engine
        pool_size = 10
        max_overflow = 100
        logger.info(
            "Creating engine with pool_size=%s and max_overflow=%s",
            pool_size,
            max_overflow,
        )
        return create_engine(
            database_url, pool_size=pool_size, max_overflow=max_overflow
        )

    def _get_message_queue(self) -> OptionalComponent[AbstractMessageQueue]:
        if self._rabbit_mq_message_queue_is_available():
            logger.info(
                "RabbitMq is available at %s",
                self._configuration.message_queue_configuration.host,
            )
            return OptionalComponent(
                RabbitMqMessageQueue(
                    self._configuration.message_queue_configuration.host
                )
            )
        return OptionalComponent.empty()

    def _rabbit_mq_message_queue_is_available(self):
        connection_parameters = pika.ConnectionParameters(
            host=self._configuration.message_queue_configuration.host
        )
        try:
            connection = pika.BlockingConnection(connection_parameters)
            if connection.is_open:
                connection.close()
                return True
        except Exception as error:
            logger.error("Error when connecting to RabbitMQ")
            logger.error(error)
            return False
