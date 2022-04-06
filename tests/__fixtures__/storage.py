import pytest

from cato_server.storage.sqlalchemy.sqlalchemy_output_repository import (
    SqlAlchemyOutputRepository,
)

# todo move sessionmaker_fixture here
from cato_server.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
)


@pytest.fixture
def sqlalchemy_output_repository(sessionmaker_fixture):
    return SqlAlchemyOutputRepository(sessionmaker_fixture)


@pytest.fixture
def sqlalchemy_suite_result_repository(sessionmaker_fixture):
    return SqlAlchemySuiteResultRepository(sessionmaker_fixture)
