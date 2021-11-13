from enum import Enum

from cato_common.domain.test_status import TestStatus


class UnifiedTestStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    def to_test_status(self):
        if self.value == "SUCCESS":
            return TestStatus.SUCCESS
        elif self.value == "FAILED":
            return TestStatus.FAILED
        raise ValueError(f"Value {self.value} is not a TestStatus!")
