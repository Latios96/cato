import logging
from dataclasses import dataclass
from typing import Type, Any

import pinject
import requests
from celery import Celery
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
from cato_server.storage.abstract.abstract_performance_trace_repository import (
    PerformanceTraceRepository,
)
from cato_server.storage.abstract.auth_user_repository import (
    AuthUserRepository,
)
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.output_repository import OutputRepository
from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.storage.abstract.run_batch_repository import RunBatchRepository
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.session_repository import SessionRepository
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
from cato_server.storage.sqlalchemy.sqlalchemy_auth_user_repository import (
    SqlAlchemyAuthUserRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_deduplicating_file_storage import (
    SqlAlchemyDeduplicatingFileStorage,
)
from cato_server.storage.sqlalchemy.sqlalchemy_image_repository import (
    SqlAlchemyImageRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_output_repository import (
    SqlAlchemyOutputRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_performance_trace_repository import (
    SqlAlchemyPerformanceTraceRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_project_repository import (
    SqlAlchemyProjectRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_run_batch_repository import (
    SqlAlchemyRunBatchRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_run_repository import (
    SqlAlchemyRunRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_session_repository import (
    SqlAlchemySessionRepository,
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
    auth_user_repository: Type[AuthUserRepository]
    session_repository: Type[SessionRepository]
    run_batch_repository: Type[RunBatchRepository]
    performance_trace_repository: Type[PerformanceTraceRepository]
    session_maker_binding: Any
    root_path_binding: str


@dataclass
class SchedulerBindings:
    scheduler_submitter_binding: OptionalComponent[AbstractSchedulerSubmitter]


@dataclass
class ConfigurationBindings:
    app_configuration: AppConfiguration


@dataclass
class TaskQueueBindings:
    celery_app: Celery


@dataclass
class Bindings:
    storage_bindings: StorageBindings
    app_configuration: AppConfiguration
    scheduler_bindings: SchedulerBindings
    configuration_bindings: ConfigurationBindings
    task_queue_bindings: TaskQueueBindings


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
            "secrets_configuration",
            to_instance=self._bindings.app_configuration.secrets_configuration,
        )
        bind(
            "storage_configuration",
            to_instance=self._bindings.configuration_bindings.app_configuration.storage_configuration,
        )
        bind(
            "logging_configuration",
            to_instance=self._bindings.configuration_bindings.app_configuration.logging_configuration,
        )
        bind(
            "celery_configuration",
            to_instance=self._bindings.configuration_bindings.app_configuration.celery_configuration,
        )
        bind(
            "scheduler_configuration",
            to_instance=self._bindings.configuration_bindings.app_configuration.scheduler_configuration,
        )
        bind(
            "sentry_configuration",
            to_instance=self._bindings.configuration_bindings.app_configuration.sentry_configuration,
        )
        bind(
            "session_configuration",
            to_instance=self._bindings.configuration_bindings.app_configuration.session_configuration,
        )
        bind(
            "oidc_configuration",
            to_instance=self._bindings.configuration_bindings.app_configuration.oidc_configuration,
        )
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
        bind(
            "auth_user_repository",
            to_class=self._bindings.storage_bindings.auth_user_repository,
        )
        bind(
            "session_repository",
            to_class=self._bindings.storage_bindings.session_repository,
        )
        bind(
            "run_batch_repository",
            to_class=self._bindings.storage_bindings.run_batch_repository,
        )
        bind(
            "performance_trace_repository",
            to_class=self._bindings.storage_bindings.performance_trace_repository,
        )

        bind("celery_app", to_instance=self._bindings.task_queue_bindings.celery_app)


class BindingsFactory:
    def __init__(self, configuration: AppConfiguration):
        self._configuration = configuration

    def create_bindings(self) -> PinjectBindings:
        logger.info("Creating bindings..")
        storage_bindings = self.create_storage_bindings()
        scheduler_bindings = self.create_scheduler_bindings()
        configuration_bindings = self.create_configuration_bindings()
        task_queue_bindings = self.create_task_queue_bindings()

        bindings = Bindings(
            storage_bindings,
            self._configuration,
            scheduler_bindings,
            configuration_bindings,
            task_queue_bindings,
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
            auth_user_repository=SqlAlchemyAuthUserRepository,
            session_repository=SqlAlchemySessionRepository,
            run_batch_repository=SqlAlchemyRunBatchRepository,
            performance_trace_repository=SqlAlchemyPerformanceTraceRepository,
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
        return create_engine(database_url)

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
                        url, DeadlineApi(url), self._configuration
                    )
                )
            logger.info('Scheduler "Deadline" is not available')
            return OptionalComponent.empty()
        logger.info(f'Scheduler is not available, unknown name "{scheduler_name}"')
        return OptionalComponent.empty()

    def _deadline_is_available(self, url: str) -> bool:
        response = requests.get(url + "/api/users?NamesOnly=true")
        return response.status_code == 200

    def create_configuration_bindings(self):
        return ConfigurationBindings(app_configuration=self._configuration)

    def create_task_queue_bindings(self):
        result_backend = (
            "db+postgresql://"
            + self._configuration.storage_configuration.database_url.split("://")[1]
        )
        celery_app = Celery(
            "tasks",
            broker=self._configuration.celery_configuration.broker_url,
            result_backend=result_backend,
        )
        return TaskQueueBindings(celery_app=celery_app)
