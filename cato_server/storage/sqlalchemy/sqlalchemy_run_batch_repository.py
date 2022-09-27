from dataclasses import dataclass
from typing import Optional, Callable

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import composite, relationship, joinedload

from cato_common.domain.run_batch_identifier import RunBatchIdentifier
from cato_common.domain.run_batch_provider import RunBatchProvider
from cato_common.domain.run_identifier import RunIdentifier
from cato_common.domain.run_name import RunName
from cato_common.storage.page import PageRequest, Page
from cato_server.domain.run_batch import RunBatch
from cato_server.storage.abstract.run_batch_repository import RunBatchRepository
from cato_server.storage.abstract.run_filter_options import RunFilterOptions
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)
from cato_server.storage.sqlalchemy.sqlalchemy_run_repository import (
    _RunMapping,
    SqlAlchemyRunRepository,
)
from cato_server.storage.sqlalchemy.type_decorators.utc_date_time import UtcDateTime


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
    created_at = Column(UtcDateTime, nullable=False)

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
            .options(self.default_query_options())
            .first()
        )
        if run_batch_mapping:
            return self.to_domain_object(run_batch_mapping)

    def find_by_project_id_with_paging(
        self,
        id: int,
        page_request: PageRequest,
        filter_options: Optional[RunFilterOptions] = None,
    ) -> Page[RunBatch]:
        with self._session_maker() as session:
            query = (
                session.query(self.mapping_cls())
                .filter(self.mapping_cls().project_entity_id == id)
                .options(self.default_query_options())
            )
            if filter_options:
                query = self._apply_filter_options(query, filter_options)

            return self._pageginate(
                session,
                query.order_by(self.mapping_cls().created_at.desc()).order_by(
                    self.mapping_cls().id.desc()
                ),
                page_request,
            )

    def _apply_filter_options(self, query, filter_options: RunFilterOptions):
        return query.filter(
            self.mapping_cls().runs.any(
                _RunMapping.branch_name.in_({x.name for x in filter_options.branches})
            )
        )

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
            created_at=domain_object.created_at,
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
            created_at=entity.created_at,
            runs=runs,
        )

    def mapping_cls(self):
        return _RunBatchMapping

    def default_query_options(self):
        return [
            joinedload(_RunBatchMapping.runs).options(
                *SqlAlchemyRunRepository.default_query_options(None)
            )
        ]
