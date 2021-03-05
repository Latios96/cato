import datetime
import os
import socketserver
from pathlib import Path
from typing import Optional, Dict

import humanfriendly
import pytest
import sqlalchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from cato.config.config_file_writer import ConfigFileWriter
from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_status import TestStatus
from cato.domain.test_suite import TestSuite
from cato_server.__main__ import create_app
from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.bindings_factory import (
    BindingsFactory,
    Bindings,
    PinjectBindings,
    MessageQueueBindings,
)
from cato_server.configuration.logging_configuration import LoggingConfiguration
from cato_server.configuration.message_queue_configuration import (
    MessageQueueConfiguration,
)
from cato_server.configuration.optional_component import OptionalComponent
from cato_server.configuration.storage_configuration import StorageConfiguration
from cato_server.domain.execution_status import ExecutionStatus
from cato_server.domain.image import Image, ImageChannel
from cato_server.domain.machine_info import MachineInfo
from cato_server.domain.output import Output
from cato_server.domain.project import Project
from cato_server.domain.run import Run
from cato_server.domain.suite_result import SuiteResult
from cato_server.domain.test_identifier import TestIdentifier
from cato_server.domain.test_result import TestResult
from cato_server.mappers.mapper_registry_factory import MapperRegistryFactory
from cato_server.mappers.object_mapper import ObjectMapper
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
    is_postgres = hasattr(dbapi_connection, "info")
    if not is_postgres:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def find_pg_ctl(ver: str) -> Optional[Path]:
    candidates = list(Path(f"/usr/lib/postgresql/{ver}/").glob("**/bin/pg_ctl"))
    if candidates:
        return candidates[0]


def postgres_available():
    ctl = find_pg_ctl("12")
    if ctl:
        return True
    print("Postgres is not available!")
    return False


databases = ["sqlite", "postgres"] if postgres_available() else ["sqlite"]


def pytest_generate_tests(metafunc):
    metafunc_module = str(metafunc.cls)
    has_connection_ficture = "db_connection" in metafunc.fixturenames
    is_storage_test = "test_abstract_sqlalchemy_repository" in metafunc_module
    if has_connection_ficture and is_storage_test:
        metafunc.parametrize("db_connection", databases)


@pytest.fixture
def db_connection():
    return "default"


if postgres_available:

    @pytest.fixture
    def db_connection_string(db_connection, postgresql):
        if "postgres" in db_connection:
            return f"postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}"
        return "sqlite:///:memory:"


else:

    @pytest.fixture
    def db_connection_string(db_connection):
        return "sqlite:///:memory:"


@pytest.fixture
def sessionmaker_fixture(db_connection_string):
    if "sqlite" in db_connection_string:
        engine = sqlalchemy.create_engine(
            db_connection_string,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    else:
        engine = sqlalchemy.create_engine(db_connection_string)
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
def test_result_factory():
    def or_default(value, default_value):
        if value is None:
            return default_value
        return value

    def factory(
        id: Optional[int] = None,
        suite_result_id: Optional[int] = None,
        test_name: Optional[str] = None,
        test_identifier: Optional[TestIdentifier] = None,
        test_command: Optional[str] = None,
        test_variables: Optional[Dict[str, str]] = None,
        machine_info: Optional[MachineInfo] = None,
        execution_status: Optional[ExecutionStatus] = None,
        status: Optional[TestStatus] = None,
        seconds: Optional[float] = None,
        message: Optional[str] = None,
        image_output: Optional[int] = None,
        reference_image: Optional[int] = Optional[int],
        started_at: Optional[datetime.datetime] = None,
        finished_at: Optional[datetime.datetime] = None,
    ):
        return TestResult(
            id=or_default(id, 0),
            suite_result_id=or_default(suite_result_id, 0),
            test_name=or_default(test_name, "my_test_name"),
            test_identifier=or_default(
                test_identifier,
                TestIdentifier(suite_name="my_suite", test_name="my_test_name"),
            ),
            test_command=or_default(test_command, "my_command"),
            test_variables=or_default(test_variables, {"testkey": "test_value"}),
            machine_info=or_default(
                machine_info, MachineInfo(cpu_name="cpu", cores=56, memory=8)
            ),
            execution_status=or_default(execution_status, ExecutionStatus.NOT_STARTED),
            status=or_default(status, TestStatus.SUCCESS),
            seconds=or_default(seconds, 5.0),
            message=or_default(message, "success"),
            image_output=or_default(image_output, None),
            reference_image=or_default(reference_image, None),
            started_at=or_default(started_at, datetime.datetime.now()),
            finished_at=or_default(finished_at, datetime.datetime.now()),
        )

    return factory


@pytest.fixture
def test_result(sessionmaker_fixture, test_result_factory, suite_result, stored_image):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    test_result = test_result_factory(
        suite_result_id=suite_result.id,
        image_output=stored_image.id,
        reference_image=stored_image.id,
    )
    return repository.save(test_result)


@pytest.fixture
def finished_test_result(
    sessionmaker_fixture, test_result_factory, suite_result, stored_image
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    test_result = test_result_factory(
        suite_result_id=suite_result.id,
        image_output=stored_image.id,
        reference_image=stored_image.id,
        execution_status=ExecutionStatus.FINISHED,
    )
    return repository.save(test_result)


@pytest.fixture()
def stored_file(sessionmaker_fixture, tmp_path, test_resource_provider):
    repository = SqlAlchemyDeduplicatingFileStorage(sessionmaker_fixture, str(tmp_path))
    return repository.save_file(test_resource_provider.resource_by_name("test.exr"))


@pytest.fixture()
def stored_file_alpha(sessionmaker_fixture, tmp_path, test_resource_provider):
    repository = SqlAlchemyDeduplicatingFileStorage(sessionmaker_fixture, str(tmp_path))
    return repository.save_file(test_resource_provider.resource_by_name("test.exr"))


@pytest.fixture()
def stored_image(sessionmaker_fixture, tmp_path, stored_file, stored_file_alpha):
    repository = SqlAlchemyImageRepository(sessionmaker_fixture)
    return repository.save(
        Image(
            id=0,
            name="test.exr",
            original_file_id=stored_file.id,
            channels=[
                ImageChannel(id=0, name="rgb", image_id=0, file_id=stored_file.id),
                ImageChannel(
                    id=0, name="alpha", image_id=0, file_id=stored_file_alpha.id
                ),
            ],
            width=1920,
            height=1080,
        )
    )


@pytest.fixture()
def output(sessionmaker_fixture, test_result):
    repository = SqlAlchemyOutputRepository(sessionmaker_fixture)
    return repository.save(
        Output(id=0, test_result_id=test_result.id, text="This is a long text")
    )


@pytest.fixture()
def output_for_finished_test(sessionmaker_fixture, finished_test_result):
    repository = SqlAlchemyOutputRepository(sessionmaker_fixture)
    return repository.save(
        Output(id=0, test_result_id=finished_test_result.id, text="This is a long text")
    )


def random_port():
    with socketserver.TCPServer(("localhost", 0), None) as s:
        random_port = s.server_address[1]
    return random_port


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
        message_queue_configuration=MessageQueueConfiguration(host="DISABLED"),
    )
    bindings_factory = BindingsFactory(config)
    storage_bindings = bindings_factory.create_storage_bindings()
    storage_bindings.session_maker_binding = sessionmaker_fixture
    message_queue_bindings = MessageQueueBindings(
        message_queue_binding=OptionalComponent.empty()
    )
    bindings = Bindings(storage_bindings, config, message_queue_bindings)
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


@pytest.fixture
def mapper_registry():
    return MapperRegistryFactory().create_mapper_registry()


@pytest.fixture
def object_mapper(mapper_registry):
    return ObjectMapper(mapper_registry)


class ConfigFixture:
    TEST = Test(
        name="My_first_test",
        command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
        variables={"frame": "7"},
    )
    TEST_SUITE = TestSuite(
        name="My_first_test_Suite",
        tests=[TEST],
        variables={"my_var": "from_suite"},
    )
    CONFIG = Config(
        project_name="EXAMPLE_PROJECT",
        path="test",
        test_suites=[TEST_SUITE],
        output_folder="output",
        variables={"my_var": "from_config"},
    )


@pytest.fixture
def config_fixture():
    return ConfigFixture


@pytest.fixture
def config_file_fixture(tmp_path, config_fixture):
    path = os.path.join(str(tmp_path), "cato.json")
    ConfigFileWriter().write_to_file(path, config_fixture.CONFIG)
    return path
