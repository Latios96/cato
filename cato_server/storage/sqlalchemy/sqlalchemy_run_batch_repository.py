from dataclasses import dataclass
from typing import Optional, Callable

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import composite, relationship

from cato_common.domain.run_batch_identifier import RunBatchIdentifier
from cato_common.domain.run_batch_provider import RunBatchProvider
from cato_common.domain.run_identifier import RunIdentifier
from cato_common.domain.run_name import RunName
from cato_server.domain.run_batch import RunBatch
from cato_server.storage.abstract.run_batch_repository import RunBatchRepository
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)
from cato_server.storage.sqlalchemy.sqlalchemy_run_repository import (
    _RunMapping,
    SqlAlchemyRunRepository,
)


@dataclass
class _RunBatchIdentifierMapping:
    provider: str
    run_name: str
    run_identifier: str

    def __composite_values__(self):
        return self.provider, self.run_name, self.run_identifier

    @staticmethod
    def from_identifier(run_batch_identifier: RunBatchIdentifier):
        return _RunBatchIdentifierMapping(
            provider=run_batch_identifier.provider.name,
            run_name=str(run_batch_identifier.run_name),
            run_identifier=str(run_batch_identifier.run_identifier),
        )

    def to_identifier(self) -> RunBatchIdentifier:
        return RunBatchIdentifier(
            provider=RunBatchProvider(self.provider),
            run_name=RunName(self.run_name),
            run_identifier=RunIdentifier(self.run_identifier),
        )


class _RunBatchMapping(Base):
    __tablename__ = "run_batch_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    provider = Column(String, nullable=False)
    run_name = Column(String, nullable=False)
    run_identifier = Column(String, nullable=False)
    project_entity_id = Column(Integer, ForeignKey("project_entity.id"), nullable=False)

    run_batch_identifier = composite(
        _RunBatchIdentifierMapping, provider, run_name, run_identifier
    )

    runs = relationship(_RunMapping)

    UniqueConstraint(
        "provider",
        "run_name",
        "run_identifier",
        "project_entity_id",
        name="uq_batch_identifier_project",
    )


class SqlAlchemyRunBatchRepository(AbstractSqlAlchemyRepository, RunBatchRepository):
    def find_by_project_id_and_run_batch_identifier(
        self, project_id: int, run_batch_identifier: RunBatchIdentifier
    ) -> Optional[RunBatch]:
        with self._session_maker() as session:
            return self._find_by_project_id_and_run_batch_identifier_impl(
                session, project_id, run_batch_identifier
            )

    def find_or_save_by_project_id_and_run_batch_identifier(
        self,
        project_id: int,
        run_batch_identifier: RunBatchIdentifier,
        run_batch_factory: Callable[[], RunBatch],
    ) -> RunBatch:
        with self._session_maker() as session:
            maybe_run_batch = self._find_by_project_id_and_run_batch_identifier_impl(
                session, project_id, run_batch_identifier
            )
            if maybe_run_batch:
                return maybe_run_batch
            run_batch = run_batch_factory()
            return self.save(run_batch)

    def _find_by_project_id_and_run_batch_identifier_impl(
        self, session, project_id: int, run_batch_identifier: RunBatchIdentifier
    ) -> Optional[RunBatch]:
        run_batch_mapping = (
            session.query(_RunBatchMapping)
            .filter(_RunBatchMapping.project_entity_id == project_id)
            .filter(
                _RunBatchMapping.run_batch_identifier
                == _RunBatchIdentifierMapping.from_identifier(run_batch_identifier)
            )
            .first()
        )
        if run_batch_mapping:
            return self.to_domain_object(run_batch_mapping)

    def to_entity(self, domain_object: RunBatch) -> _RunBatchMapping:
        runs = list(
            map(
                lambda x: SqlAlchemyRunRepository.to_entity(None, x), domain_object.runs
            )
        )
        return _RunBatchMapping(
            id=domain_object.id if domain_object.id else None,
            run_batch_identifier=_RunBatchIdentifierMapping.from_identifier(
                domain_object.run_batch_identifier
            ),
            project_entity_id=domain_object.project_id,
            runs=runs,
        )

    def to_domain_object(self, entity: _RunBatchMapping) -> RunBatch:
        runs = list(
            map(
                lambda x: SqlAlchemyRunRepository.to_domain_object(None, x), entity.runs
            )
        )
        return RunBatch(
            id=entity.id,
            run_batch_identifier=entity.run_batch_identifier.to_identifier(),
            project_id=entity.project_entity_id,
            runs=runs,
        )

    def mapping_cls(self):
        return _RunBatchMapping
