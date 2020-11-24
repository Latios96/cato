import datetime
import os
import uuid

import attr
from sqlalchemy import Column, Integer, String, create_engine, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


@attr.s
class Project:
    id: int = attr.ib()
    name: str = attr.ib()


@attr.s
class Run:
    id: int = attr.ib()
    project_id: int = attr.ib()
    started_at: datetime.datetime = attr.ib()


class ProjectRepository:
    def save(self, project: Project) -> Project:
        raise NotImplementedError()


__Base = declarative_base()


class _ProjectMapping(__Base):
    __tablename__ = "project_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)


class ProjectSqlAlchemyRepository(ProjectRepository):
    def __init__(self, session_maker):
        self._session_maker = session_maker

    def save(self, project: Project) -> Project:
        session = self._session_maker()

        project_mapping = _ProjectMapping(
            id=project.id if project.id else None, name=project.name
        )

        session.add(project_mapping)
        session.flush()

        project = Project(id=project_mapping.id, name=project.name)

        session.commit()
        session.close()

        return project


class TestResultMapping(__Base):
    __tablename__ = "test_result_entity"
    id = Column("id", Integer, primary_key=True)
    suite_result_entity_id = Column("suite_result_entity_id", Integer)
    output = Column("output", JSON(), nullable=True)
    test_variables = Column("test_variables", JSON(), nullable=True)
    test_name = Column("test_name", String(), nullable=False)
    test_command = Column("test_command", String(), nullable=False)
    execution_status = Column("execution_status", String(), nullable=False)


if __name__ == "__main__":
    engine = create_engine(
        "postgresql+psycopg2://postgres:postgres@localhost:5432/cato-dev", echo=True
    )
    Session = sessionmaker(bind=engine)
    repo = ProjectSqlAlchemyRepository(Session)
    print(repo.save(Project(id=0, name=str(uuid.uuid4()))))

    result = TestResultMapping(
        id=0,
        suite_result_entity_id=2,
        output=["line {}".format(x) for x in range(10)],
        test_variables=dict(os.environ),
        test_name="tse",
        test_command="tt",
        execution_status="NOT_STARTED",
    )
    session = Session()
    session.add(result)
    session.flush()
    session.commit()
    session.close()
