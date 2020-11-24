import datetime

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from cato.domain.project import Project
from cato.domain.run import Run
from cato.storage.sqlalchemy.abstract_sqlalchemy_repository import Base
from cato.storage.sqlalchemy.sqlalchemy_project_repository import (
    SqlAlchemyProjectRepository,
)
from cato.storage.sqlalchemy.sqlalchemy_run_repository import SqlAlchemyRunRepository


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
