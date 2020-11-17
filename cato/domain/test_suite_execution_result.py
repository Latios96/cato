from dataclasses import dataclass
from typing import List

from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_result import TestStatus
from cato.domain.test_suite import TestSuite


@dataclass
class TestSuiteExecutionResult:
    test_suite: TestSuite
    result: TestStatus
    test_results: List[TestExecutionResult]

    def to_dict(self):
        return {
            'test_suite': self.test_suite.to_dict(),
            'result': str(self.result),
            'test_results': [x.to_dict() for x in self.test_results]
        }
