from cato_common.domain.performance_trace import PerformanceTrace
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class PerformanceTraceRepository(AbstractRepository[PerformanceTrace, int]):
    pass
