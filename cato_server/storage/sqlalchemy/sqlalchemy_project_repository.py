from typing import Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from cato_common.domain.project import Project, ProjectStatus
from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class _ProjectMapping(Base):
    __tablename__ = "project_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True)
    status = Column(String, nullable=False)
    thumbnail_file_entity_id = Column(
        Integer, ForeignKey("file_entity.id"), nullable=True
    )

    runs = relationship("_RunMapping", backref="project")


class SqlAlchemyProjectRepository(AbstractSqlAlchemyRepository, ProjectRepository):
    def find_by_name(self, name: str) -> Optional[Project]:
        session = self._session_maker()

        project = (
            session.query(_ProjectMapping).filter(_ProjectMapping.name == name).first()
        )
        session.close()
        if project:
            return self.to_domain_object(project)

    def to_entity(self, domain_object: Project) -> _ProjectMapping:
        return _ProjectMapping(
            id=domain_object.id if domain_object.id else None,
            name=domain_object.name,
            status=domain_object.status,
            thumbnail_file_entity_id=domain_object.thumbnail_file_id,
        )

    def to_domain_object(self, entity: _ProjectMapping) -> Project:
        return Project(
            id=entity.id,
            name=entity.name,
            status=ProjectStatus(entity.status),
            thumbnail_file_id=entity.thumbnail_file_entity_id,
        )

    def mapping_cls(self):
        return _ProjectMapping
