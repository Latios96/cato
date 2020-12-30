from typing import Optional

from cato.domain.test_status import TestStatus
from cato_server.mappers.abstract_value_mapper import AbstractValueMapper


class TestStatusValueMapper(AbstractValueMapper[TestStatus, str]):
    def map_from(self, status: Optional[str]) -> Optional[TestStatus]:
        if not status:
            return None
        values = {"SUCCESS": TestStatus.SUCCESS, "FAILED": TestStatus.FAILED}
        return values[status]

    def map_to(self, status: TestStatus) -> str:
        return status.name
