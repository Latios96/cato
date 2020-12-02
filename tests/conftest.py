import datetime

import pytest
from random_open_port import random_port
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from cato.domain.project import Project
from cato.domain.run import Run
from cato.storage.domain.suite_result import SuiteResult
from cato.storage.sqlalchemy.abstract_sqlalchemy_repository import Base
from cato.storage.sqlalchemy.sqlalchemy_project_repository import (
    SqlAlchemyProjectRepository,
)
from cato.storage.sqlalchemy.sqlalchemy_run_repository import SqlAlchemyRunRepository
from cato.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
)
from cato_server.__main__ import create_app
from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.bindings_factory import (
    BindingsFactory,
    Bindings,
    PinjectBindings,
)
from cato_server.configuration.storage_configuration import StorageConfiguration


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture
def sessionmaker_fixture():
    engine = create_engine("sqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)


@pytest.fixture
def project(sessionmaker_fixture):
    repository = SqlAlchemyProjectRepository(sessionmaker_fixture)
    project = Project(id=0, name="test_name")
    return repository.save(project)


@pytest.fixture
def run(sessionmaker_fixture, project):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    run = Run(id=0, project_id=project.id, started_at=datetime.datetime.now())
    return repository.save(run)


@pytest.fixture
def suite_result(sessionmaker_fixture, run):
    repository = SqlAlchemySuiteResultRepository(sessionmaker_fixture)
    suite_result = SuiteResult(
        id=0, run_id=run.id, suite_name="my_suite", suite_variables={"key": "value"}
    )
    return repository.save(suite_result)


@pytest.fixture()
def app_fixture(sessionmaker_fixture, tmp_path):
    config = AppConfiguration(
        port=random_port(),
        debug=True,
        storage_configuration=StorageConfiguration(
            database_url="sqlite:///:memory:", file_storage_url=str(tmp_path)
        ),
    )
    bindings_factory = BindingsFactory(config)
    storage_bindings = bindings_factory.create_storage_bindings()
    storage_bindings.session_maker_binding = sessionmaker_fixture
    bindings = Bindings(storage_bindings)
    pinject_bindings = PinjectBindings(bindings)

    app = create_app(config, pinject_bindings)

    return app


@pytest.fixture
def client(app_fixture):
    with app_fixture.test_client() as client:
        yield client
