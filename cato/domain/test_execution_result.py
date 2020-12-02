import datetime
from dataclasses import dataclass
from typing import List, Optional

from cato.domain.test import Test
from cato.domain.test_result import TestStatus


@dataclass
class TestExecutionResult:
    test: Test
    status: TestStatus
    output: List[str]
    seconds: float
    message: str
    image_output: Optional[str]
    reference_image: Optional[str]
    started_at: datetime.datetime
    finished_at: datetime.datetime

    def to_dict(self):
        return {
            "test": self.test.to_dict(),
            "status": str(self.status),
            "output": self.output,
            "seconds": self.seconds,
            "message": self.message,
            "image_output": self.image_output,
        }

    __test__ = False
