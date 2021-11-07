import logging
from dataclasses import dataclass
from typing import Type, Any

import pinject
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.optional_component import OptionalComponent
from cato_common.mappers.mapper_registry_factory import MapperRegistryFactory
from cato_server.schedulers.abstract_scheduler_submitter import (
    AbstractSchedulerSubmitter,
)
from cato_server.schedulers.deadline.deadline_api import DeadlineApi
from cato_server.schedulers.deadline.deadline_scheduler_submitter import (
    DeadlineSchedulerSubmitter,
)
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.output_repository import OutputRepository
from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.submission_info_repository import (
    SubmissionInfoRepository,
)
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.abstract.test_edit_repository import TestEditRepository
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
from cato_server.storage.sqlalchemy.sqlalchemy_submission_info_repository import (
    SqlAlchemySubmissionInfoRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_edit_repository import (
    SqlAlchemyTestEditRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_heartbeat_repository import (
    SqlAlchemyTestHeartbeatRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)

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
    submission_info_repository: Type[SubmissionInfoRepository]
    test_edit_repository: Type[TestEditRepository]
    session_maker_binding: Any
    root_path_binding: str


@dataclass
class SchedulerBindings:
    scheduler_submitter_binding: OptionalComponent[AbstractSchedulerSubmitter]


@dataclass
class Bindings:
    storage_bindings: StorageBindings
    app_configuration: AppConfiguration
    scheduler_bindings: SchedulerBindings


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
        bind(
            "mapper_registry",
            to_instance=MapperRegistryFactory().create_mapper_registry(),
        )
        bind(
            "scheduler_submitter",
            to_instance=self._bindings.scheduler_bindings.scheduler_submitter_binding,
        )
        bind(
            "submission_info_repository",
            to_class=self._bindings.storage_bindings.submission_info_repository,
        )
        bind(
            "test_edit_repository",
            to_class=self._bindings.storage_bindings.test_edit_repository,
        )


class BindingsFactory:
    def __init__(self, configuration: AppConfiguration):
        self._configuration = configuration

    def create_bindings(self) -> PinjectBindings:
        logger.info("Creating bindings..")
        storage_bindings = self.create_storage_bindings()
        scheduler_bindings = self.create_scheduler_bindings()
        bindings = Bindings(
            storage_bindings,
            self._configuration,
            scheduler_bindings,
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
            submission_info_repository=SqlAlchemySubmissionInfoRepository,
            test_edit_repository=SqlAlchemyTestEditRepository,
            root_path_binding=self._configuration.storage_configuration.file_storage_url,
            session_maker_binding=self._get_session_maker(),
        )

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

    def create_scheduler_bindings(self):
        return SchedulerBindings(
            scheduler_submitter_binding=self._create_scheduler_submitter()
        )

    def _create_scheduler_submitter(self):
        scheduler_name = self._configuration.scheduler_configuration.name
        if not scheduler_name or scheduler_name == "None":
            logger.info(f'Scheduler with name "{scheduler_name}" is not available')
            return OptionalComponent.empty()
        if scheduler_name == "Deadline":
            url = self._configuration.scheduler_configuration.url
            logger.info('Probing scheduler "Deadline"...')
            if self._deadline_is_available(url):
                logger.info(
                    'Scheduler "Deadline" is available at %s',
                    url,
                )
                return OptionalComponent(
                    DeadlineSchedulerSubmitter(
                        url,
                        DeadlineApi(url),
                    )
                )
            logger.info('Scheduler "Deadline" is not available')
            return OptionalComponent.empty()
        logger.info(f'Scheduler is not available, unknown name "{scheduler_name}"')
        return OptionalComponent.empty()

    def _deadline_is_available(self, url: str) -> bool:
        response = requests.get(url + "/api/users?NamesOnly=true")
        return response.status_code == 200
