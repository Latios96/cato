from typing import Optional

from sqlalchemy import Column, Integer, Text

from cato_common.domain.performance_trace import PerformanceTrace
from cato_server.storage.abstract.abstract_performance_trace_repository import (
    PerformanceTraceRepository,
)
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)
from cato_server.storage.sqlalchemy.sqlalchemy_run_repository import _RunMapping


class PerformanceTraceMapping(Base):
    __tablename__ = "performance_trace_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    performance_trace_json = Column(Text, nullable=False)


class SqlAlchemyPerformanceTraceRepository(
    AbstractSqlAlchemyRepository[PerformanceTrace, PerformanceTraceMapping, int],
    PerformanceTraceRepository,
):
    def to_entity(self, domain_object: PerformanceTrace) -> PerformanceTraceMapping:
        return PerformanceTraceMapping(
            id=domain_object.id if domain_object.id else None,
            performance_trace_json=domain_object.performance_trace_json,
        )

    def to_domain_object(self, entity: PerformanceTraceMapping) -> PerformanceTrace:
        return PerformanceTrace(
            id=entity.id, performance_trace_json=entity.performance_trace_json
        )

    def mapping_cls(self):
        return PerformanceTraceMapping

    def find_by_run_id(self, run_id: int) -> Optional[PerformanceTrace]:
        session = self._session_maker()

        query = (
            session.query(self.mapping_cls())
            .join(_RunMapping)
            .filter(_RunMapping.id == run_id)
            .options(self.default_query_options())
        )
        return self._map_one_to_domain_object(query.first())
