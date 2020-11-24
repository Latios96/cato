from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from cato.domain.run import Run
from cato.storage.abstract.run_repository import RunRepository
from cato.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class _RunMapping(Base):
    __tablename__ = "run_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_entity_id = Column(Integer, ForeignKey("project_entity.id"))
    started_at = Column(DateTime)

    suite_results = relationship("_SuiteResultMapping", backref="run")


class SqlAlchemyRunRepository(AbstractSqlAlchemyRepository, RunRepository):
    def to_entity(self, domain_object: Run) -> _RunMapping:
        return _RunMapping(
            id=domain_object.id if domain_object.id else None,
            project_entity_id=domain_object.project_id,
            started_at=domain_object.started_at,
        )

    def to_domain_object(self, entity: _RunMapping) -> Run:
        return Run(
            id=entity.id,
            project_id=entity.project_entity_id,
            started_at=entity.started_at,
        )

    def mapping_cls(self):
        return _RunMapping
