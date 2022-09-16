import pytest

from cato_common.config.config_file_parser import JsonConfigParser
from cato_common.config.config_file_writer import ConfigFileWriter
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

# todo move sessionmaker_fixture here
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
from cato_server.storage.sqlalchemy.sqlalchemy_simple_file_storage import (
    SqlAlchemySimpleFileStorage,
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


@pytest.fixture
def sqlalchemy_project_repository(sessionmaker_fixture):
    return SqlAlchemyProjectRepository(sessionmaker_fixture)


@pytest.fixture
def sqlalchemy_output_repository(sessionmaker_fixture):
    return SqlAlchemyOutputRepository(sessionmaker_fixture)


@pytest.fixture
def sqlalchemy_suite_result_repository(sessionmaker_fixture):
    return SqlAlchemySuiteResultRepository(sessionmaker_fixture)


@pytest.fixture
def sqlalchemy_session_repository(sessionmaker_fixture):
    return SqlAlchemySessionRepository(sessionmaker_fixture)


@pytest.fixture
def sqlalchemy_image_repository(sessionmaker_fixture):
    return SqlAlchemyImageRepository(sessionmaker_fixture)


@pytest.fixture
def sqlalchemy_test_heartbeat_repository(sessionmaker_fixture):
    return SqlAlchemyTestHeartbeatRepository(sessionmaker_fixture)


@pytest.fixture
def sqlalchemy_test_result_repository(sessionmaker_fixture):
    return SqlAlchemyTestResultRepository(sessionmaker_fixture)


@pytest.fixture
def sqlalchemy_auth_user_repository(sessionmaker_fixture):
    return SqlAlchemyAuthUserRepository(sessionmaker_fixture)


@pytest.fixture
def sqlalchemy_run_repository(sessionmaker_fixture):
    return SqlAlchemyRunRepository(sessionmaker_fixture)


@pytest.fixture
def sqlalchemy_test_edit_repository(sessionmaker_fixture):
    return SqlAlchemyTestEditRepository(sessionmaker_fixture)


@pytest.fixture
def sqlalchemy_submission_info_repository(sessionmaker_fixture, object_mapper):
    return SqlAlchemySubmissionInfoRepository(
        sessionmaker_fixture, JsonConfigParser(), ConfigFileWriter(object_mapper)
    )


@pytest.fixture
def sqlalchemy_simple_file_storage(sessionmaker_fixture, tmp_path):
    return SqlAlchemySimpleFileStorage(sessionmaker_fixture, str(tmp_path))


@pytest.fixture
def sqlalchemy_deduplicating_storage(sessionmaker_fixture, tmp_path):
    return SqlAlchemyDeduplicatingFileStorage(sessionmaker_fixture, str(tmp_path))


@pytest.fixture
def sqlalchemy_run_batch_repository(
    sessionmaker_fixture,
) -> SqlAlchemyRunBatchRepository:
    return SqlAlchemyRunBatchRepository(sessionmaker_fixture)
