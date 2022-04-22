import pytest

from cato.config.config_file_parser import JsonConfigParser
from cato.config.config_file_writer import ConfigFileWriter
from cato_server.storage.sqlalchemy.session_provider import SessionProvider
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

# todo move session_provider here
from cato_server.storage.sqlalchemy.sqlalchemy_project_repository import (
    SqlAlchemyProjectRepository,
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
def sqlalchemy_project_repository(session_provider_with_session):
    return SqlAlchemyProjectRepository(session_provider_with_session)


@pytest.fixture
def sqlalchemy_output_repository(session_provider_with_session):
    return SqlAlchemyOutputRepository(session_provider_with_session)


@pytest.fixture
def sqlalchemy_suite_result_repository(session_provider_with_session):
    return SqlAlchemySuiteResultRepository(session_provider_with_session)


@pytest.fixture
def sqlalchemy_session_repository(session_provider_with_session):
    return SqlAlchemySessionRepository(session_provider_with_session)


@pytest.fixture
def sqlalchemy_image_repository(session_provider_with_session):
    return SqlAlchemyImageRepository(session_provider_with_session)


@pytest.fixture
def sqlalchemy_test_heartbeat_repository(session_provider_with_session):
    return SqlAlchemyTestHeartbeatRepository(session_provider_with_session)


@pytest.fixture
def sqlalchemy_test_result_repository(session_provider_with_session):
    return SqlAlchemyTestResultRepository(session_provider_with_session)


@pytest.fixture
def sqlalchemy_auth_user_repository(session_provider_with_session):
    return SqlAlchemyAuthUserRepository(session_provider_with_session)


@pytest.fixture
def sqlalchemy_run_repository(session_provider_with_session):
    return SqlAlchemyRunRepository(session_provider_with_session)


@pytest.fixture
def sqlalchemy_test_edit_repository(session_provider_with_session):
    return SqlAlchemyTestEditRepository(session_provider_with_session)


@pytest.fixture
def sqlalchemy_submission_info_repository(session_provider_with_session, object_mapper):
    return SqlAlchemySubmissionInfoRepository(
        session_provider_with_session,
        JsonConfigParser(),
        ConfigFileWriter(object_mapper),
    )


@pytest.fixture
def sqlalchemy_simple_file_storage(session_provider_with_session, tmp_path):
    return SqlAlchemySimpleFileStorage(session_provider_with_session, str(tmp_path))


@pytest.fixture
def sqlalchemy_deduplicating_storage(session_provider_with_session, tmp_path):
    return SqlAlchemyDeduplicatingFileStorage(
        session_provider_with_session, str(tmp_path)
    )
