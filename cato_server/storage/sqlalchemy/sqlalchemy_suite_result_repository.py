from collections import defaultdict
from typing import Optional, List, Set, Dict

from sqlalchemy import Column, Integer, ForeignKey, String, JSON, func
from sqlalchemy.orm import relationship

from cato_common.storage.page import PageRequest, Page
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_common.domain.suite_result import SuiteResult
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class _SuiteResultMapping(Base):
    __tablename__ = "suite_result_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_entity_id = Column(Integer, ForeignKey("run_entity.id"), nullable=False)
    suite_name = Column(String, nullable=False)
    suite_variables = Column(JSON, nullable=False)

    test_results = relationship("_TestResultMapping", backref="suite_result")


class SqlAlchemySuiteResultRepository(
    AbstractSqlAlchemyRepository, SuiteResultRepository
):
    def to_entity(self, domain_object: SuiteResult) -> _SuiteResultMapping:
        return _SuiteResultMapping(
            id=domain_object.id if domain_object.id else None,
            run_entity_id=domain_object.run_id,
            suite_name=domain_object.suite_name,
            suite_variables=domain_object.suite_variables,
        )

    def to_domain_object(self, entity: _SuiteResultMapping) -> SuiteResult:
        return SuiteResult(
            id=entity.id,
            run_id=entity.run_entity_id,
            suite_name=entity.suite_name,
            suite_variables=entity.suite_variables,
        )

    def mapping_cls(self):
        return _SuiteResultMapping

    def find_by_run_id(self, run_id: int) -> List[SuiteResult]:
        session = self._session_maker()

        entities = self._order_by_case_insensitive(
            session.query(self.mapping_cls()).filter(
                self.mapping_cls().run_entity_id == run_id
            ),
            self.mapping_cls().suite_name,
        ).all()
        session.close()
        return list(map(self.to_domain_object, entities))

    def find_by_run_id_with_paging(
        self, run_id: int, page_request: PageRequest
    ) -> Page[SuiteResult]:
        session = self._session_maker()

        page = self._pageginate(
            session,
            self._order_by_case_insensitive(
                session.query(self.mapping_cls()).filter(
                    self.mapping_cls().run_entity_id == run_id
                ),
                self.mapping_cls().suite_name,
            ),
            page_request,
        )
        session.close()
        return page

    def find_by_run_id_and_name(self, run_id: int, name: str) -> Optional[SuiteResult]:
        session = self._session_maker()

        entity = (
            session.query(self.mapping_cls())
            .filter(self.mapping_cls().run_entity_id == run_id)
            .filter(self.mapping_cls().suite_name == name)
            .first()
        )
        session.close()
        if entity:
            return self.to_domain_object(entity)
        return None

    def suite_count_by_run_ids(self, run_ids: Set[int]) -> Dict[int, int]:
        with self._session_maker() as session:
            suite_result_counts = (
                session.query(
                    _SuiteResultMapping.run_entity_id,
                    func.count(_SuiteResultMapping.id),
                )
                .filter(self.mapping_cls().run_entity_id.in_(run_ids))
                .group_by(_SuiteResultMapping.run_entity_id)
                .all()
            )

            counts_by_run_id = defaultdict(lambda: 0)
            counts_by_run_id.update(
                {
                    run_id: suite_result_count
                    for run_id, suite_result_count in suite_result_counts
                }
            )
            return counts_by_run_id
