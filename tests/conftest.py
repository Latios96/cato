import datetime
import os
import socketserver
import sqlite3
import tempfile
import uuid
from pathlib import Path
from typing import Optional, Dict, List, Tuple

import humanfriendly
import pytest
import sqlalchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from starlette.testclient import TestClient

from cato_common.config.config_file_writer import ConfigFileWriter
from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.config import Config, RunConfig
from cato_common.domain.performance_trace import PerformanceTrace
from cato_common.domain.run_batch_identifier import RunBatchIdentifier
from cato_common.domain.run_batch_provider import RunBatchProvider
from cato_common.domain.run_identifier import RunIdentifier
from cato_common.domain.run_name import RunName
from cato_common.domain.test import Test
from cato_common.domain.test_suite import TestSuite
from cato_api_client.cato_api_client import CatoApiClient
from cato_api_client.http_template import HttpTemplate
from cato_common.domain.auth.email import Email
from cato_common.domain.auth.username import Username
from cato_common.domain.branch_name import BranchName
from cato_common.domain.file import File
from cato_common.domain.image import Image, ImageChannel, ImageTranscodingState
from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.output import Output
from cato_common.domain.project import Project, ProjectStatus
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.run import (
    Run,
)
from cato_common.domain.run_information import (
    OS,
    BasicRunInformation,
    LocalComputerRunInformation,
    GithubActionsRunInformation,
)
from cato_common.domain.submission_info import SubmissionInfo
from cato_common.domain.suite_result import SuiteResult
from cato_common.domain.test_edit import (
    ComparisonSettingsEdit,
    ComparisonSettingsEditValue,
    ReferenceImageEdit,
    ReferenceImageEditValue,
)
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.test_result import TestResult
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.dtos.run_aggregate import RunProgress, RunAggregate
from cato_common.mappers.generic_class_mapper import GenericClassMapper
from cato_common.mappers.mapper_registry_factory import MapperRegistryFactory
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.configuration.parts.celery_configuration import CeleryConfiguration
from cato_server.configuration.parts.oiio_configuration import OiioConfiguration
from cato_server.domain.run_batch import RunBatch
from cato_server.domain.run_status import RunStatus
from cato_server.startup import create_app
from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.bindings_factory import (
    BindingsFactory,
    Bindings,
    PinjectBindings,
    SchedulerBindings,
    TaskQueueBindings,
)
from cato_server.configuration.parts.logging_configuration import LoggingConfiguration
from cato_server.configuration.oidc_config import OidcConfiguration
from cato_server.configuration.optional_component import OptionalComponent
from cato_server.configuration.parts.scheduler_configuration import (
    SchedulerConfiguration,
)
from cato_server.configuration.parts.secrets_configuration import SecretsConfiguration
from cato_server.configuration.parts.sentry_configuration import SentryConfiguration
from cato_server.configuration.parts.session_configuration import SessionConfiguration
from cato_server.configuration.parts.storage_configuration import StorageConfiguration
from cato_server.domain.auth.auth_user import AuthUser
from cato_server.domain.auth.secret_str import SecretStr
from cato_server.schedulers.abstract_scheduler_submitter import (
    AbstractSchedulerSubmitter,
)
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator
from cato_common.utils.datetime_utils import aware_now_in_utc
from tests.__fixtures__.authentication_fixtures import (  # noqa: F401
    http_session_factory,
    http_session,
    http_session_cookie_factory,
    http_session_cookie,
    client_with_session,
    fixed_api_token_str,
    api_token_str_factory,
    api_token_str,
    fixed_api_token,
    fixed_http_session,
    request_factory,
    env_with_api_token,
    crsf_token_factory,
    crsf_token,
)
from tests.__fixtures__.celery_mock import MockCeleryApp
from tests.__fixtures__.storage.repositories import (  # noqa: F401
    sqlalchemy_output_repository,
    sqlalchemy_suite_result_repository,
    sqlalchemy_project_repository,
    sqlalchemy_session_repository,
    sqlalchemy_image_repository,
    sqlalchemy_test_heartbeat_repository,
    sqlalchemy_test_result_repository,
    sqlalchemy_auth_user_repository,
    sqlalchemy_run_repository,
    sqlalchemy_test_edit_repository,
    sqlalchemy_submission_info_repository,
    sqlalchemy_simple_file_storage,
    sqlalchemy_deduplicating_storage,
    sqlalchemy_run_batch_repository,
    sqlalchemy_performance_trace_repository,
)
from tests.utils import mock_safe, or_default


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
    metafunc_module = str(metafunc.module)
    has_connection_ficture = "db_connection" in metafunc.fixturenames
    is_storage_test = "cato_server.storage" in metafunc_module
    if has_connection_ficture and is_storage_test:
        metafunc.parametrize("db_connection", databases)


@pytest.fixture
def db_connection():
    return "default"


if postgres_available():

    @pytest.fixture
    def db_connection_string(db_connection, postgresql):
        if "postgres" in db_connection:
            return f"postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}"
        return "sqlite:///:memory:"

else:

    @pytest.fixture
    def db_connection_string(db_connection):
        return "sqlite:///:memory:"


def _split_and_keep_delimiter(str_to_split, delimiter):
    splitted = str_to_split.split(delimiter)
    return list(map(lambda x: x + delimiter, splitted))


@pytest.fixture(scope="session")
def sqlite_schema_statements():
    with tempfile.TemporaryDirectory() as tmpdirname:
        db_path = os.path.join(tmpdirname, "foo.db")
        sqlite_url = f"sqlite:///{db_path}"
        print(db_path)
        db_migrator = DbMigrator(
            StorageConfiguration(file_storage_url="", database_url=sqlite_url)
        )
        db_migrator.migrate()

        con = sqlite3.connect(db_path)
        schema = "\n".join(con.iterdump())
        con.close()

    schema_statements = _split_and_keep_delimiter(schema, ";")[:-2]
    yield schema_statements


@pytest.fixture
def sqlalchemy_engine(db_connection_string):
    if "sqlite" in db_connection_string:
        return sqlalchemy.create_engine(
            db_connection_string,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    return sqlalchemy.create_engine(db_connection_string)


@pytest.fixture
def sessionmaker_fixture(
    db_connection_string, sqlalchemy_engine, sqlite_schema_statements
):
    if "sqlite" in db_connection_string:
        for statement in sqlite_schema_statements:
            sqlalchemy_engine.execute(statement)
        return sessionmaker(bind=sqlalchemy_engine)

    db_migrator = DbMigrator(
        StorageConfiguration(file_storage_url="", database_url=db_connection_string)
    )
    db_migrator.migrate()
    return sessionmaker(bind=sqlalchemy_engine)


@pytest.fixture
def project_factory():
    def func(name: Optional[str] = None, status=ProjectStatus.ACTIVE):
        return Project(
            id=0,
            name=or_default(name, "test_name"),
            status=or_default(status, ProjectStatus.ACTIVE),
        )

    return func


@pytest.fixture
def saving_project_factory(sqlalchemy_project_repository, project_factory):
    def func(name: Optional[str] = None):
        return sqlalchemy_project_repository.save(project_factory(name))

    return func


@pytest.fixture
def project(saving_project_factory):
    return saving_project_factory()


@pytest.fixture
def run_factory(saving_run_batch_factory, local_computer_run_information):
    def func(
        id=None,
        project_id=None,
        run_batch_id=None,
        started_at=None,
        branch_name: BranchName = None,
        run_information: BasicRunInformation = None,
        performance_trace_id=None,
    ):
        return Run(
            id=or_default(id, 0),
            project_id=or_default(project_id, 1),
            run_batch_id=or_default(
                run_batch_id, lambda: saving_run_batch_factory().id
            ),
            created_at=or_default(started_at, aware_now_in_utc()),
            branch_name=or_default(branch_name, BranchName("default")),
            previous_run_id=None,
            run_information=or_default(run_information, local_computer_run_information),
            performance_trace_id=or_default(performance_trace_id, None),
        )

    return func


@pytest.fixture
def saving_run_factory(sqlalchemy_run_repository, project, run_factory):
    def func(
        project_id=None,
        run_batch_id=None,
        started_at=None,
        run_information: BasicRunInformation = None,
    ):
        run = run_factory(
            project_id=or_default(project_id, project.id),
            run_batch_id=run_batch_id,
            started_at=started_at,
            run_information=run_information,
        )
        return sqlalchemy_run_repository.save(run)

    return func


@pytest.fixture
def run_batch_factory(project, run_batch_identifier_factory):
    def func(
        run_batch_identifier: Optional[RunBatchIdentifier] = None,
        project_id: Optional[int] = None,
        created_at: Optional[datetime.datetime] = None,
        runs: Optional[List[Run]] = None,
    ):
        return RunBatch(
            id=0,
            run_batch_identifier=or_default(
                run_batch_identifier, run_batch_identifier_factory()
            ),
            project_id=or_default(project_id, project.id),
            created_at=or_default(created_at, aware_now_in_utc()),
            runs=or_default(runs, []),
        )

    return func


@pytest.fixture
def saving_run_batch_factory(sqlalchemy_run_batch_repository, run_batch_factory):
    def func(
        run_batch_identifier: Optional[RunBatchIdentifier] = None,
        project_id: Optional[int] = None,
        created_at: Optional[datetime.datetime] = None,
        runs: Optional[List[Run]] = None,
    ):
        return sqlalchemy_run_batch_repository.save(
            run_batch_factory(run_batch_identifier, project_id, created_at, runs)
        )

    return func


@pytest.fixture
def run_batch_with_run(
    project, run_factory, saving_run_batch_factory
) -> Tuple[RunBatch, Run]:
    run_batch = saving_run_batch_factory(runs=[run_factory(project_id=project.id)])
    yield run_batch, run_batch.runs[0]


@pytest.fixture
def run(run_batch_with_run) -> Run:
    run_batch, run = run_batch_with_run
    return run


@pytest.fixture
def run_batch(saving_run_batch_factory) -> RunBatch:
    return saving_run_batch_factory(runs=[])


@pytest.fixture
def run_batch_identifier():
    return RunBatchIdentifier(
        provider=RunBatchProvider.LOCAL_COMPUTER,
        run_name=RunName("mac-os"),
        run_identifier=RunIdentifier("3046812908-1"),
    )


@pytest.fixture
def run_batch_identifier_factory():
    def func():
        return RunBatchIdentifier(
            provider=RunBatchProvider.LOCAL_COMPUTER,
            run_name=RunName("mac-os"),
            run_identifier=RunIdentifier(str(uuid.uuid4())),
        )

    return func


@pytest.fixture
def suite_result_factory():
    def func(run_id=None, suite_name=None, suite_variables=None):
        return SuiteResult(
            id=0,
            run_id=run_id,
            suite_name=or_default(suite_name, "my_suite"),
            suite_variables=or_default(suite_variables, {"key": "value"}),
        )

    return func


@pytest.fixture
def saving_suite_result_factory(
    sqlalchemy_suite_result_repository, run, suite_result_factory
):
    def func(run_id=None, suite_name=None, suite_variables=None):
        suite_result = suite_result_factory(
            run_id=or_default(run_id, run.id),
            suite_name=or_default(suite_name, "my_suite"),
            suite_variables=or_default(suite_variables, {"key": "value"}),
        )
        return sqlalchemy_suite_result_repository.save(suite_result)

    return func


@pytest.fixture
def suite_result(sqlalchemy_suite_result_repository, run):
    suite_result = SuiteResult(
        id=0, run_id=run.id, suite_name="my_suite", suite_variables={"key": "value"}
    )
    return sqlalchemy_suite_result_repository.save(suite_result)


@pytest.fixture
def test_result_factory():
    def factory(
        id: Optional[int] = None,
        suite_result_id: Optional[int] = None,
        test_name: Optional[str] = None,
        test_identifier: Optional[TestIdentifier] = None,
        test_command: Optional[str] = None,
        test_variables: Optional[Dict[str, str]] = None,
        machine_info: Optional[MachineInfo] = None,
        unified_test_status: Optional[UnifiedTestStatus] = None,
        seconds: Optional[float] = None,
        message: Optional[str] = None,
        image_output: Optional[int] = None,
        reference_image: Optional[int] = None,
        diff_image: Optional[int] = None,
        started_at: Optional[datetime.datetime] = None,
        finished_at: Optional[datetime.datetime] = None,
        error_value=None,
        comparison_settings=None,
        thumbnail_file_id: Optional[int] = None,
        failure_reason: Optional[TestFailureReason] = None,
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
            unified_test_status=or_default(
                unified_test_status, UnifiedTestStatus.NOT_STARTED
            ),
            seconds=or_default(seconds, 5.0),
            message=or_default(message, "success"),
            image_output=or_default(image_output, None),
            reference_image=or_default(reference_image, None),
            diff_image=or_default(diff_image, None),
            started_at=or_default(started_at, aware_now_in_utc()),
            finished_at=or_default(finished_at, aware_now_in_utc()),
            comparison_settings=comparison_settings,
            error_value=or_default(error_value, None),
            thumbnail_file_id=or_default(thumbnail_file_id, None),
            failure_reason=or_default(failure_reason, None),
        )

    return factory


@pytest.fixture
def saving_test_result_factory(
    test_result_factory, suite_result, sqlalchemy_test_result_repository
):
    def func(
        id: Optional[int] = None,
        suite_result_id: Optional[int] = None,
        test_name: Optional[str] = None,
        test_identifier: Optional[TestIdentifier] = None,
        test_command: Optional[str] = None,
        test_variables: Optional[Dict[str, str]] = None,
        machine_info: Optional[MachineInfo] = None,
        unified_test_status: Optional[UnifiedTestStatus] = None,
        seconds: Optional[float] = None,
        message: Optional[str] = None,
        image_output: Optional[int] = None,
        reference_image: Optional[int] = None,
        diff_image: Optional[int] = None,
        started_at: Optional[datetime.datetime] = None,
        finished_at: Optional[datetime.datetime] = None,
        error_value=None,
        comparison_settings=None,
        thumbnail_file_id: Optional[int] = None,
        failure_reason: Optional[TestFailureReason] = None,
    ):
        test_result = test_result_factory(
            id,
            suite_result_id,
            test_name,
            test_identifier,
            test_command,
            test_variables,
            machine_info,
            unified_test_status,
            seconds,
            message,
            image_output,
            reference_image,
            diff_image,
            started_at,
            finished_at,
            error_value,
            comparison_settings,
            thumbnail_file_id,
            failure_reason,
        )
        return sqlalchemy_test_result_repository.save(test_result)

    return func


@pytest.fixture
def test_result(
    sqlalchemy_test_result_repository, test_result_factory, suite_result, stored_image
):
    test_result = test_result_factory(
        suite_result_id=suite_result.id,
        image_output=stored_image.id,
        reference_image=stored_image.id,
        diff_image=stored_image.id,
    )
    return sqlalchemy_test_result_repository.save(test_result)


@pytest.fixture
def machine_info():
    return MachineInfo(cpu_name="cpu", cores=56, memory=8)


@pytest.fixture
def test_edit(sqlalchemy_test_edit_repository, test_result, stored_image_factory):
    test_edit = ComparisonSettingsEdit(
        id=0,
        test_id=test_result.id,
        test_identifier=test_result.test_identifier,
        created_at=aware_now_in_utc(),
        old_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1
            ),
            status=ResultStatus.SUCCESS,
            message=test_result.message,
            diff_image_id=test_result.diff_image,
            error_value=1,
        ),
        new_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=10
            ),
            status=ResultStatus.SUCCESS,
            message="still " + test_result.message,
            diff_image_id=stored_image_factory().id,
            error_value=0.1,
        ),
    )
    return sqlalchemy_test_edit_repository.save(test_edit)


@pytest.fixture
def test_result_no_machine_info(
    sessionmaker_fixture,
    sqlalchemy_test_result_repository,
    test_result_factory,
    suite_result,
    stored_image,
):
    test_result = test_result_factory(
        suite_result_id=suite_result.id,
        image_output=stored_image.id,
        reference_image=stored_image.id,
    )
    test_result.machine_info = None
    return sqlalchemy_test_result_repository.save(test_result)


@pytest.fixture
def finished_test_result(
    sqlalchemy_test_result_repository, test_result_factory, suite_result, stored_image
):
    test_result = test_result_factory(
        suite_result_id=suite_result.id,
        image_output=stored_image.id,
        reference_image=stored_image.id,
        unified_test_status=UnifiedTestStatus.SUCCESS,
    )
    return sqlalchemy_test_result_repository.save(test_result)


@pytest.fixture()
def stored_file(sqlalchemy_deduplicating_storage, test_resource_provider):
    return sqlalchemy_deduplicating_storage.save_file(
        test_resource_provider.resource_by_name("test.exr")
    )


@pytest.fixture()
def stored_file_factory():
    def func(id=0):
        return File(
            id=id,
            name="test.exr",
            hash="c9e76fde29d88e42dbc9b4a28c4b1eed67d8cb1247715768f9ca1ac5f3f3d5f1",
            value_counter=0,
        )

    return func


@pytest.fixture()
def stored_file_alpha(sqlalchemy_deduplicating_storage, test_resource_provider):
    return sqlalchemy_deduplicating_storage.save_file(
        test_resource_provider.resource_by_name("test.exr")
    )


@pytest.fixture()
def stored_image_factory(
    sqlalchemy_image_repository, tmp_path, stored_file, stored_file_alpha
):
    def func(id=0):
        return sqlalchemy_image_repository.save(
            Image(
                id=id,
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
                transcoding_state=ImageTranscodingState.TRANSCODED,
            )
        )

    return func


@pytest.fixture()
def stored_image(stored_image_factory):
    return stored_image_factory()


@pytest.fixture()
def output(sqlalchemy_output_repository, test_result):
    return sqlalchemy_output_repository.save(
        Output(id=0, test_result_id=test_result.id, text="This is a long text")
    )


@pytest.fixture()
def performance_trace(sqlalchemy_performance_trace_repository):
    return sqlalchemy_performance_trace_repository.save(
        PerformanceTrace(
            id=0,
            performance_trace_json="""{"traceEvents":[{"name":"Cato Run","ph":"B","pid":0,"tid":0,"ts":0.0},{"name":"Create run in DB","ph":"B","pid":0,"tid":0,"ts":0.0},{"name":"Create run in DB","ph":"E","pid":0,"tid":0,"ts":122204.5},{"name":"Suite exr","ph":"B","pid":0,"tid":0,"ts":122204.5},{"name":"Test exr/exr_singlechannel_16_bit","ph":"B","pid":0,"tid":0,"ts":122204.5},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":122204.5},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":1523898.25},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":1552367.75},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":1612882.5},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":1615882.5},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":1882379.25},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":1882379.25},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":3007458.5},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":3007458.5},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":4136254.5},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":4136254.5},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":5265385.5},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":5266385.0},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":5314464.75},{"name":"Test exr/exr_singlechannel_16_bit","ph":"E","pid":0,"tid":0,"ts":5314464.75},{"name":"Test exr/exr_singlechannel_32_bit","ph":"B","pid":0,"tid":0,"ts":5314464.75},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":5314464.75},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":5335464.0},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":5364463.5},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":5435005.75},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":5436006.0},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":5739956.5},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":5739956.5},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":6896781.75},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":6896781.75},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":8052670.75},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":8052670.75},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":9179739.5},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":9179739.5},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":9226739.5},{"name":"Test exr/exr_singlechannel_32_bit","ph":"E","pid":0,"tid":0,"ts":9226739.5},{"name":"Test exr/exr_multichannel_16_bit_1080p","ph":"B","pid":0,"tid":0,"ts":9226739.5},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":9226739.5},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":9248468.25},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":9275476.25},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":9346476.5},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":9347476.5},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":11645006.0},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":11645006.0},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":14261094.0},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":14261094.0},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":16861761.5},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":16861761.5},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":18025417.75},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":18026418.5},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":18073941.25},{"name":"Test exr/exr_multichannel_16_bit_1080p","ph":"E","pid":0,"tid":0,"ts":18073941.25},{"name":"Test exr/exr_multichannel_16_bit","ph":"B","pid":0,"tid":0,"ts":18073941.25},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":18073941.25},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":18095935.75},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":18124449.0},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":18189316.5},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":18190316.25},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":19979901.25},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":19979901.25},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":28698599.25},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":28698599.25},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":37419699.75},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":37419699.75},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":38570678.25},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":38571678.25},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":38618680.75},{"name":"Test exr/exr_multichannel_16_bit","ph":"E","pid":0,"tid":0,"ts":38618680.75},{"name":"Suite exr","ph":"E","pid":0,"tid":0,"ts":38618680.75},{"name":"Suite jpg","ph":"B","pid":0,"tid":0,"ts":38618680.75},{"name":"Test jpg/jpeg","ph":"B","pid":0,"tid":0,"ts":38618680.75},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":38618680.75},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":38641678.75},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":38669209.0},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":38730218.75},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":38730218.75},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":38885054.0},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":38885054.0},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":41046643.5},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":41046643.5},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":42163911.25},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":42163911.25},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":43299748.75},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":43299748.75},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":43346921.25},{"name":"Test jpg/jpeg","ph":"E","pid":0,"tid":0,"ts":43347918.5},{"name":"Suite jpg","ph":"E","pid":0,"tid":0,"ts":43347918.5},{"name":"Suite png","ph":"B","pid":0,"tid":0,"ts":43347918.5},{"name":"Test png/png_8_bit","ph":"B","pid":0,"tid":0,"ts":43347918.5},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":43347918.5},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":43369918.5},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":43398435.25},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":43461347.75},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":43461347.75},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":43667947.25},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":43667947.25},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":44800511.0},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":44800511.0},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":45943589.5},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":45943589.5},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":47069490.5},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":47070490.0},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":47117492.0},{"name":"Test png/png_8_bit","ph":"E","pid":0,"tid":0,"ts":47117492.0},{"name":"Test png/png_16_bit","ph":"B","pid":0,"tid":0,"ts":47117492.0},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":47117492.0},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":47139498.5},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":47167498.0},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":47228928.5},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":47229458.75},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":47502471.75},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":47502471.75},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":48650610.0},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":48650610.0},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":49795284.25},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":49795284.25},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":50949031.75},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":50950031.5},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":50997010.25},{"name":"Test png/png_16_bit","ph":"E","pid":0,"tid":0,"ts":50997010.25},{"name":"Suite png","ph":"E","pid":0,"tid":0,"ts":50997010.25},{"name":"Suite tiff","ph":"B","pid":0,"tid":0,"ts":50997010.25},{"name":"Test tiff/tiff_8_bit","ph":"B","pid":0,"tid":0,"ts":50998008.75},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":50998008.75},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":51019007.0},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":51046017.0},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":51108419.25},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":51109419.25},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":51308107.75},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":51308107.75},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":52470686.0},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":52470686.0},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":53640037.25},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":53640037.25},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":54774310.0},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":54775310.75},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":54823425.5},{"name":"Test tiff/tiff_8_bit","ph":"E","pid":0,"tid":0,"ts":54823425.5},{"name":"Test tiff/tiff_16_bit","ph":"B","pid":0,"tid":0,"ts":54823425.5},{"name":"start test request","ph":"B","pid":0,"tid":0,"ts":54823425.5},{"name":"start test request","ph":"E","pid":0,"tid":0,"ts":54845425.25},{"name":"test command execution","ph":"B","pid":0,"tid":0,"ts":54873436.25},{"name":"test command execution","ph":"E","pid":0,"tid":0,"ts":54938036.75},{"name":"image comparison","ph":"B","pid":0,"tid":0,"ts":54939035.75},{"name":"image comparison","ph":"E","pid":0,"tid":0,"ts":55176540.75},{"name":"upload reference image","ph":"B","pid":0,"tid":0,"ts":55176540.75},{"name":"upload reference image","ph":"E","pid":0,"tid":0,"ts":56377314.0},{"name":"upload output image","ph":"B","pid":0,"tid":0,"ts":56377314.0},{"name":"upload output image","ph":"E","pid":0,"tid":0,"ts":57576304.5},{"name":"upload diff image","ph":"B","pid":0,"tid":0,"ts":57576304.5},{"name":"upload diff image","ph":"E","pid":0,"tid":0,"ts":58716805.75},{"name":"finish test request","ph":"B","pid":0,"tid":0,"ts":58717806.25},{"name":"finish test request","ph":"E","pid":0,"tid":0,"ts":58763937.0},{"name":"Test tiff/tiff_16_bit","ph":"E","pid":0,"tid":0,"ts":58763937.0},{"name":"Suite tiff","ph":"E","pid":0,"tid":0,"ts":58763937.0},{"name":"Cato Run","ph":"E","pid":0,"tid":0,"ts":58763937.0}]}""",
        )
    )


@pytest.fixture()
def output_for_finished_test(sqlalchemy_output_repository, finished_test_result):
    return sqlalchemy_output_repository.save(
        Output(id=0, test_result_id=finished_test_result.id, text="This is a long text")
    )


@pytest.fixture()
def submission_info(
    sqlalchemy_submission_info_repository, run, config_fixture, object_mapper
):
    sub_info = SubmissionInfo(
        id=0,
        config=config_fixture.CONFIG,
        run_id=run.id,
        resource_path="resource_path",
        executable="executable",
    )
    return sqlalchemy_submission_info_repository.save(sub_info)


@pytest.fixture
def local_computer_run_information():
    return LocalComputerRunInformation(
        id=0, run_id=0, os=OS.WINDOWS, computer_name="cray", local_username="username"
    )


@pytest.fixture
def github_actions_run_information():
    return GithubActionsRunInformation(
        id=0,
        run_id=0,
        os=OS.LINUX,
        computer_name="cray",
        github_run_id=3052454707,
        html_url="https://github.com/owner/repo-name/actions/runs/3052454707/jobs/4921861789",
        job_name="build_ubuntu",
        actor="Latios96",
        attempt=1,
        run_number=2,
        github_url="https://github.com",
        github_api_url="https://api.github.com",
    )


@pytest.fixture
def auth_user(sqlalchemy_auth_user_repository):
    auth_user = AuthUser(
        id=0,
        username=Username("username"),
        fullname=Username("User Username"),
        email=Email("foo@bar.com"),
    )
    return sqlalchemy_auth_user_repository.save(auth_user)


@pytest.fixture
def run_aggregate_factory(local_computer_run_information: LocalComputerRunInformation):
    def func(
        id: Optional[int] = None,
        project_id: Optional[int] = None,
        started_at: Optional[datetime.datetime] = None,
        status: Optional[RunStatus] = None,
        duration: Optional[float] = None,
        branch_name: Optional[BranchName] = None,
        run_information: Optional[BasicRunInformation] = None,
        suite_count: Optional[int] = None,
        test_count: Optional[int] = None,
        progress: Optional[RunProgress] = None,
    ):
        return RunAggregate(
            id=or_default(
                id,
                1,
            ),
            project_id=or_default(project_id, 1),
            created_at=or_default(
                started_at, datetime.datetime(year=2022, month=9, day=30)
            ),
            status=or_default(
                status,
                RunStatus.SUCCESS,
            ),
            duration=or_default(
                duration,
                1,
            ),
            branch_name=or_default(
                branch_name,
                BranchName(name="main"),
            ),
            run_information=or_default(run_information, local_computer_run_information),
            suite_count=or_default(
                suite_count,
                1,
            ),
            test_count=or_default(
                test_count,
                10,
            ),
            progress=or_default(
                progress,
                RunProgress(
                    waiting_test_count=1,
                    running_test_count=2,
                    failed_test_count=3,
                    succeeded_test_count=4,
                    progress_percentage=0.9,
                ),
            ),
            performance_trace_id=None,
        )

    return func


def random_port():
    with socketserver.TCPServer(("localhost", 0), None) as s:
        random_port = s.server_address[1]
    return random_port


@pytest.fixture()
def mocked_scheduler_submitter():
    return mock_safe(AbstractSchedulerSubmitter)


@pytest.fixture
def oidc_configuration():
    return OidcConfiguration(
        client_id="client-id",
        client_secret=SecretStr("secret"),
        well_known_url="http://somewhere",
    )


@pytest.fixture
def celery_binding():
    return MockCeleryApp()


@pytest.fixture()
def app_and_config_fixture(
    sessionmaker_fixture,
    tmp_path,
    mocked_scheduler_submitter,
    oidc_configuration,
    celery_binding,
    db_connection_string,
):
    port = random_port()
    config = AppConfiguration(
        port=port,
        debug=True,
        secrets_configuration=SecretsConfiguration(
            sessions_secret=SecretStr("SESSIONS_SECRET"),
            csrf_secret=SecretStr("CSRF_SECRET"),
            api_tokens_secret=SecretStr("API_TOKENS_SECRET"),
        ),
        hostname=f"localhost",
        public_url=f"http://127.0.0.1:{port}",
        workers=16,
        storage_configuration=StorageConfiguration(
            database_url=db_connection_string, file_storage_url=str(tmp_path)
        ),
        logging_configuration=LoggingConfiguration(
            "log.txt", False, humanfriendly.parse_size("10mb"), 10
        ),
        scheduler_configuration=SchedulerConfiguration(),
        sentry_configuration=SentryConfiguration.default(),
        session_configuration=SessionConfiguration.default(),
        oidc_configuration=oidc_configuration,
        celery_configuration=CeleryConfiguration(broker_url="test"),
        oiio_configuration=OiioConfiguration(thread_count=1),
    )
    bindings_factory = BindingsFactory(config)
    storage_bindings = bindings_factory.create_storage_bindings()
    storage_bindings.session_maker_binding = sessionmaker_fixture
    scheduler_bindings = SchedulerBindings(
        scheduler_submitter_binding=OptionalComponent(mocked_scheduler_submitter)
    )
    bindings = Bindings(
        storage_bindings,
        config,
        scheduler_bindings,
        configuration_bindings=bindings_factory.create_configuration_bindings(),
        task_queue_bindings=TaskQueueBindings(
            bindings_factory.create_task_queue_bindings().celery_app
            if not celery_binding
            else celery_binding
        ),
    )
    pinject_bindings = PinjectBindings(bindings)

    app = create_app(config, pinject_bindings)

    return app, config


@pytest.fixture
def app_fixture(app_and_config_fixture):
    app, config = app_and_config_fixture
    return app


@pytest.fixture
def client(app_fixture):
    return TestClient(app_fixture)


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
    generic_class_mapper = GenericClassMapper(mapper_registry)
    return ObjectMapper(generic_class_mapper)


class ConfigFixture:
    def __init__(self):
        self.TEST = Test(
            name="My_first_test",
            command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
            variables={"frame": "7"},
            comparison_settings=ComparisonSettings.default(),
        )
        self.TEST_SUITE = TestSuite(
            name="My_first_test_Suite",
            tests=[self.TEST],
            variables={"my_var": "from_suite"},
        )
        self.CONFIG = Config(
            project_name="EXAMPLE_PROJECT",
            suites=[self.TEST_SUITE],
            variables={"my_var": "from_config"},
        )
        self.RUN_CONFIG = RunConfig(
            project_name="EXAMPLE_PROJECT",
            resource_path="test",
            suites=[self.TEST_SUITE],
            output_folder="output",
            variables={"my_var": "from_config"},
        )


@pytest.fixture
def config_fixture():
    return ConfigFixture()


@pytest.fixture
def config_file_fixture(tmp_path, config_fixture):
    path = os.path.join(str(tmp_path), "cato.json")
    ConfigFileWriter().write_to_file(path, config_fixture.CONFIG)
    return path


@pytest.fixture
def saving_comparison_settings_edit_factory(
    stored_image_factory, sqlalchemy_test_edit_repository
):
    def func(test_id, created_at):
        return sqlalchemy_test_edit_repository.save(
            ComparisonSettingsEdit(
                id=0,
                test_id=test_id,
                test_identifier=TestIdentifier.from_string("some/test"),
                created_at=created_at,
                new_value=ComparisonSettingsEditValue(
                    comparison_settings=ComparisonSettings(
                        method=ComparisonMethod.SSIM, threshold=1
                    ),
                    status=ResultStatus.SUCCESS,
                    message=None,
                    diff_image_id=stored_image_factory().id,
                    error_value=1,
                ),
                old_value=ComparisonSettingsEditValue(
                    comparison_settings=ComparisonSettings(
                        method=ComparisonMethod.SSIM, threshold=0.5
                    ),
                    status=ResultStatus.FAILED,
                    message="Failed",
                    diff_image_id=stored_image_factory().id,
                    error_value=0.5,
                ),
            )
        )

    return func


@pytest.fixture
def saving_reference_image_edit_factory(
    stored_image_factory, sqlalchemy_test_edit_repository
):
    def func(test_id, created_at):
        return sqlalchemy_test_edit_repository.save(
            ReferenceImageEdit(
                id=0,
                test_id=test_id,
                test_identifier=TestIdentifier.from_string("some/test"),
                created_at=created_at,
                new_value=ReferenceImageEditValue(
                    status=ResultStatus.SUCCESS,
                    message=None,
                    reference_image_id=stored_image_factory().id,
                    diff_image_id=stored_image_factory().id,
                    error_value=1,
                ),
                old_value=ReferenceImageEditValue(
                    status=ResultStatus.FAILED,
                    message="Failed",
                    reference_image_id=stored_image_factory().id,
                    diff_image_id=stored_image_factory().id,
                    error_value=0.5,
                ),
            )
        )

    return func


@pytest.fixture
def cato_api_client(app_and_config_fixture, client, object_mapper, api_token_str):
    pp, config = app_and_config_fixture
    api_client = CatoApiClient(
        f"http://localhost:{config.port}",
        HttpTemplate(object_mapper, client),
        object_mapper,
        api_token_provider=lambda: api_token_str,
    )
    return api_client
