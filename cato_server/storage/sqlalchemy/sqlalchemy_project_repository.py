from typing import Optional

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from cato.domain.project import Project
from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class _ProjectMapping(Base):
    __tablename__ = "project_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)

    runs = relationship("_RunMapping", backref="project")


class SqlAlchemyProjectRepository(AbstractSqlAlchemyRepository, ProjectRepository):
    def find_by_name(self, name: str) -> Optional[Project]:
        session = self._session_maker()

        project = (
            session.query(_ProjectMapping).filter(_ProjectMapping.name == name).first()
        )
        if project:
            return self.to_domain_object(project)

    def to_entity(self, domain_object: Project) -> _ProjectMapping:
        return _ProjectMapping(
            id=domain_object.id if domain_object.id else None, name=domain_object.name
        )

    def to_domain_object(self, entity: _ProjectMapping) -> Project:
        return Project(id=entity.id, name=entity.name)

    def mapping_cls(self):
        return _ProjectMapping
