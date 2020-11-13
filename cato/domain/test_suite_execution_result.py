from dataclasses import dataclass

from cato.domain.test_result import TestResult
from cato.domain.test_suite import TestSuite


@dataclass
class TestSuiteExecutionResult:
    test_suite: TestSuite
    result: TestResult
