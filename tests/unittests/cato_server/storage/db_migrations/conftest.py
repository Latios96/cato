import pytest
import sqlalchemy
from sqlalchemy.pool import StaticPool


@pytest.fixture
def mapped_db_connection_string(tmp_path, db_connection_string):
    if "sqlite" in db_connection_string:
        return f"sqlite:///{tmp_path / 'test.sqlite'}".replace("\\", "/")
    return db_connection_string


@pytest.fixture
def engine(mapped_db_connection_string):
    if "sqlite" in mapped_db_connection_string:
        engine = sqlalchemy.create_engine(
            mapped_db_connection_string,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
    else:
        engine = sqlalchemy.create_engine(mapped_db_connection_string)
    return engine
