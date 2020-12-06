from typing import Optional

from cato.mappers.abstract_value_mapper import AbstractValueMapper
from cato_server.storage.domain.execution_status import ExecutionStatus


class ExecutionStatusValueMapper(AbstractValueMapper[ExecutionStatus, str]):
    def map_from(self, status: Optional[str]) -> Optional[ExecutionStatus]:
        if not status:
            return None
        return {
            "NOT_STARTED": ExecutionStatus.NOT_STARTED,
            "RUNNING": ExecutionStatus.RUNNING,
            "FINISHED": ExecutionStatus.FINISHED,
        }[status]

    def map_to(self, status: ExecutionStatus) -> str:
        return status.name
