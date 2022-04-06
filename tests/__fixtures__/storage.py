import pytest

from cato_server.storage.sqlalchemy.sqlalchemy_output_repository import (
    SqlAlchemyOutputRepository,
)

# todo move sessionmaker_fixture here
@pytest.fixture
def sqlalchemy_output_repository(sessionmaker_fixture):
    return SqlAlchemyOutputRepository(sessionmaker_fixture)
