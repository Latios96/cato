import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from cato.storage.sqlalchemy.abstract_sqlalchemy_repository import Base


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
