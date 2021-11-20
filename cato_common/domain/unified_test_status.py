from enum import Enum

from cato_common.domain.result_status import ResultStatus


class UnifiedTestStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    def to_result_status(self) -> ResultStatus:
        if self.value == "SUCCESS":
            return ResultStatus.SUCCESS
        elif self.value == "FAILED":
            return ResultStatus.FAILED
        raise ValueError(f"Value {self.value} is not a TestStatus!")
