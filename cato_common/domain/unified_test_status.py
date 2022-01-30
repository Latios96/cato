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
        raise ValueError(f"Value {self.value} is not a ResultStatus!")

    @staticmethod
    def from_result_status(result_status):
        # type: (ResultStatus)->UnifiedTestStatus
        if result_status == "SUCCESS":
            return UnifiedTestStatus.SUCCESS
        elif result_status == "FAILED":
            return UnifiedTestStatus.FAILED
        raise ValueError(
            f"Value {result_status} can not be mapped to UnifiedTestStatus"
        )
