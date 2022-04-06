import pytest

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
from cato_server.storage.sqlalchemy.sqlalchemy_session_repository import (
    SqlAlchemySessionRepository,
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
