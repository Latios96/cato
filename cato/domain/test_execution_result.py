from dataclasses import dataclass
from typing import List

from cato.domain.test import Test
from cato.domain.test_result import TestStatus


@dataclass
class TestExecutionResult:
    test: Test
    status: TestStatus  # todo rename to status
    output: List[str]
    seconds: float
    message: str
    image_output: str

    def to_dict(self):
        return {
            "test": self.test.to_dict(),
            "status": str(self.status),
            "output": self.output,
            "seconds": self.seconds,
            "message": self.message,
            "image_output": self.image_output,
        }
