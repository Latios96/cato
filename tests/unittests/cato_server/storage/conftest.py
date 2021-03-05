import pytest
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import Base


def pytest_generate_tests(metafunc):
    if "db_connection" in metafunc.fixturenames:
        metafunc.parametrize("db_connection", ["sqlite", "postgres"])


@pytest.fixture
def db_connection():
    return "default"


@pytest.fixture
def db_connection_string(db_connection, postgresql):
    if "postgres" in db_connection:
        return f"postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}"
    return "sqlite:///:memory:"


@pytest.fixture
def storage_test_sessionmaker(db_connection_string):
    engine = sqlalchemy.create_engine(
        db_connection_string,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)
