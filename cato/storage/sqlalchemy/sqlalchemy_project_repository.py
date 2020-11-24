from typing import Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from cato.domain.project import Project
from cato.storage.abstract.abstract_repository import K
from cato.storage.abstract.project_repository import ProjectRepository
from cato.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    E,
    T,
)

Base = declarative_base()


class _ProjectMapping(Base):
    __tablename__ = "project_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)


class SqlAlchemyProjectRepository(ProjectRepository, AbstractSqlAlchemyRepository):
    def save(self, project: Project) -> Project:
        session = self._session_maker()

        project_mapping = _ProjectMapping(
            id=project.id if project.id else None, name=project.name
        )

        session.add(project_mapping)
        session.flush()

        project = self.to_domain_object(project_mapping)

        session.commit()
        session.close()

        return project

    def find_by_name(self, name: str) -> Optional[Project]:
        session = self._session_maker()

        project = (
            session.query(_ProjectMapping).filter(_ProjectMapping.name == name).first()
        )
        if project:
            return self.to_domain_object(project)

    def find_by_id(self, id: int) -> Optional[Project]:
        session = self._session_maker()

        project = (
            session.query(_ProjectMapping).filter(_ProjectMapping.id == id).first()
        )
        if project:
            return self.to_domain_object(project)

    def to_entity(self, domain_object: Project) -> _ProjectMapping:
        return _ProjectMapping(id=domain_object.id, name=domain_object.name)

    def to_domain_object(self, entity: _ProjectMapping) -> Project:
        return Project(id=entity.id, name=entity.name)
