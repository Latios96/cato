import datetime
import os

import humanfriendly
import pytest
from random_open_port import random_port
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from cato.domain.execution_status import ExecutionStatus
from cato.domain.image import Image, ImageChannel
from cato.domain.machine_info import MachineInfo
from cato.domain.output import Output
from cato.domain.project import Project
from cato.domain.run import Run
from cato.domain.suite_result import SuiteResult
from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_result import TestResult
from cato.domain.test_status import TestStatus
from cato_server.__main__ import create_app
from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.bindings_factory import (
    BindingsFactory,
    Bindings,
    PinjectBindings,
)
from cato_server.configuration.logging_configuration import LoggingConfiguration
from cato_server.configuration.storage_configuration import StorageConfiguration
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
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)


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


@pytest.fixture
def test_result(sessionmaker_fixture, suite_result, stored_image):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    test_result = TestResult(
        id=0,
        suite_result_id=suite_result.id,
        test_name="my_test_name",
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test_name"),
        test_command="my_command",
        test_variables={"testkey": "test_value"},
        machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
        execution_status=ExecutionStatus.NOT_STARTED,
        status=TestStatus.SUCCESS,
        seconds=5,
        message="sucess",
        image_output=stored_image.id,
        reference_image=stored_image.id,
        started_at=datetime.datetime.now(),
        finished_at=datetime.datetime.now(),
    )
    return repository.save(test_result)


@pytest.fixture()
def stored_file(sessionmaker_fixture, tmp_path):
    repository = SqlAlchemyDeduplicatingFileStorage(sessionmaker_fixture, str(tmp_path))
    return repository.save_file(os.path.join(os.path.dirname(__file__), "test.exr"))


@pytest.fixture()
def stored_image(sessionmaker_fixture, tmp_path, stored_file):
    repository = SqlAlchemyImageRepository(sessionmaker_fixture)
    return repository.save(
        Image(
            id=0,
            name="test.exr",
            original_file_id=stored_file.id,
            channels=[
                ImageChannel(id=0, name="rgb", image_id=0, file_id=stored_file.id)
            ],
        )
    )


@pytest.fixture()
def output(sessionmaker_fixture, test_result):
    repository = SqlAlchemyOutputRepository(sessionmaker_fixture)
    return repository.save(
        Output(id=0, test_result_id=test_result.id, text="This is a long text")
    )


@pytest.fixture()
def app_and_config_fixture(sessionmaker_fixture, tmp_path):
    config = AppConfiguration(
        port=random_port(),
        debug=True,
        storage_configuration=StorageConfiguration(
            database_url="sqlite:///:memory:", file_storage_url=str(tmp_path)
        ),
        logging_configuration=LoggingConfiguration(
            "log.txt", False, humanfriendly.parse_size("10mb"), 10
        ),
    )
    bindings_factory = BindingsFactory(config)
    storage_bindings = bindings_factory.create_storage_bindings()
    storage_bindings.session_maker_binding = sessionmaker_fixture
    bindings = Bindings(storage_bindings, config)
    pinject_bindings = PinjectBindings(bindings)

    app = create_app(config, pinject_bindings)

    return app, config


@pytest.fixture
def app_fixture(app_and_config_fixture):
    app, config = app_and_config_fixture
    return app


@pytest.fixture
def client(app_fixture):
    with app_fixture.test_client() as client:
        yield client


@pytest.fixture
def test_resource_provider():
    class TestResourceProvider:
        def __init__(self, root):
            self._root = root

        def resource_by_name(self, name):
            return os.path.join(self._root, name)

    return TestResourceProvider(os.path.join(os.path.dirname(__file__), "resources"))
