from typing import List, Optional

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy_utc import UtcDateTime

from cato_common.domain.branch_name import BranchName
from cato_common.domain.run import Run
from cato_common.storage.page import PageRequest, Page
from cato_server.storage.abstract.run_filter_options import RunFilterOptions
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class _RunMapping(Base):
    __tablename__ = "run_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_entity_id = Column(Integer, ForeignKey("project_entity.id"))
    started_at = Column(UtcDateTime)
    branch_name = Column(String, nullable=False)
    previous_run_id = Column(Integer, ForeignKey("run_entity.id"), nullable=True)

    suite_results = relationship("_SuiteResultMapping", backref="run")


class SqlAlchemyRunRepository(AbstractSqlAlchemyRepository, RunRepository):
    def to_entity(self, domain_object: Run) -> _RunMapping:
        return _RunMapping(
            id=domain_object.id if domain_object.id else None,
            project_entity_id=domain_object.project_id,
            started_at=domain_object.started_at,
            branch_name=str(domain_object.branch_name),
            previous_run_id=domain_object.previous_run_id,
        )

    def to_domain_object(self, entity: _RunMapping) -> Run:
        return Run(
            id=entity.id,
            project_id=entity.project_entity_id,
            started_at=entity.started_at,
            branch_name=BranchName(entity.branch_name),
            previous_run_id=entity.previous_run_id,
        )

    def mapping_cls(self):
        return _RunMapping

    def find_by_project_id(self, id: int) -> List[Run]:
        session = self._session_maker()

        entities = (
            session.query(self.mapping_cls())
            .filter(self.mapping_cls().project_entity_id == id)
            .order_by(self.mapping_cls().started_at.desc())
            .order_by(self.mapping_cls().id.desc())
            .all()
        )

        session.close()
        return list(map(self.to_domain_object, entities))

    def find_by_project_id_with_paging(
        self,
        id: int,
        page_request: PageRequest,
        filter_options: Optional[RunFilterOptions] = None,
    ) -> Page[Run]:
        session = self._session_maker()

        query = session.query(self.mapping_cls()).filter(
            self.mapping_cls().project_entity_id == id
        )
        if filter_options:
            query = self._apply_filter_options(query, filter_options)
        page = self._pageginate(
            session,
            query.order_by(self.mapping_cls().started_at.desc()).order_by(
                self.mapping_cls().id.desc()
            ),
            page_request,
        )

        session.close()
        return page

    def find_last_run_for_project(
        self, project_id: int, branch_name: BranchName
    ) -> Optional[Run]:
        session = self._session_maker()

        query = (
            session.query(_RunMapping)
            .filter(_RunMapping.project_entity_id == project_id)
            .filter(_RunMapping.branch_name == branch_name.name)
            .order_by(_RunMapping.id.desc())
        )
        session.close()
        return self._map_one_to_domain_object(query.first())

    def _apply_filter_options(self, query, filter_options: RunFilterOptions):
        return query.filter(
            self.mapping_cls().branch_name.in_(
                {x.name for x in filter_options.branches}
            )
        )

    def find_branches_for_project(self, project_id: int) -> List[BranchName]:
        session = self._session_maker()

        query = (
            session.query(_RunMapping.branch_name)
            .distinct()
            .filter(_RunMapping.project_entity_id == project_id)
        )
        query = self._order_by_case_insensitive(query, _RunMapping.branch_name)
        branch_names = query.all()
        session.close()

        return [BranchName(x[0]) for x in branch_names]
