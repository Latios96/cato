from dataclasses import dataclass
from typing import Type, Any

import pinject
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cato.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato.storage.abstract.abstract_test_result_repository import TestResultRepository
from cato.storage.abstract.project_repository import ProjectRepository
from cato.storage.abstract.run_repository import RunRepository
from cato.storage.abstract.suite_result_repository import SuiteResultRepository
from cato.storage.sqlalchemy.abstract_sqlalchemy_repository import Base
from cato.storage.sqlalchemy.sqlalchemy_deduplicating_file_storage import (
    SqlAlchemyDeduplicatingFileStorage,
)
from cato.storage.sqlalchemy.sqlalchemy_project_repository import (
    SqlAlchemyProjectRepository,
)
from cato.storage.sqlalchemy.sqlalchemy_run_repository import SqlAlchemyRunRepository
from cato.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
)
from cato.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)
from cato_server.configuration.app_configuration import AppConfiguration

import logging
logger = logging.getLogger(__name__)

FILE_STORAGE_IN_MEMORY = ":memory:"

@dataclass
class StorageBindings:
    project_repository_binding: Type[ProjectRepository]
    run_repository_binding: Type[RunRepository]
    suite_result_repository_binding: Type[SuiteResultRepository]
    test_result_repository_binding: Type[TestResultRepository]
    file_storage_binding: Type[AbstractFileStorage]
    session_maker_binding: Any
    root_path_binding: str


@dataclass
class Bindings:
    storage_bindings: StorageBindings


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
        bind("root_path", to_instance=self._bindings.storage_bindings.root_path_binding)
        bind(
            "session_maker",
            to_instance=self._bindings.storage_bindings.session_maker_binding,
        )


class BindingsFactory:
    def __init__(self, configuration: AppConfiguration):
        self._configuration = configuration

    def create_bindings(self) -> PinjectBindings:
        logger.info("Creating bindings..")
        storage_bindings = self.create_storage_bindings()
        bindings = Bindings(storage_bindings)
        return PinjectBindings(bindings)

    def create_storage_bindings(self):
        logger.info("Creating storage bindings..")
        return StorageBindings(
            project_repository_binding=SqlAlchemyProjectRepository,
            run_repository_binding=SqlAlchemyRunRepository,
            suite_result_repository_binding=SqlAlchemySuiteResultRepository,
            test_result_repository_binding=SqlAlchemyTestResultRepository,
            file_storage_binding=SqlAlchemyDeduplicatingFileStorage,
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
        max_overflow = 20
        logger.info("Creating engine with pool_size=%s and max_overflow=%s", pool_size, max_overflow)
        return create_engine(database_url, pool_size=pool_size, max_overflow=max_overflow)
