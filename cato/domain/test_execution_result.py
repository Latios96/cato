from dataclasses import dataclass
from typing import List

from cato.domain.test import Test
from cato.domain.test_result import TestStatus


@dataclass
class TestExecutionResult:
    test: Test
    result: TestStatus
    output: List[str]
    seconds: float
    message: str

    def to_dict(self):
        return {
            'test': self.test.to_dict(),
            'result': str(self.result),
            'output': self.output,
            'seconds': self.seconds,
            'message': self.message
        }
