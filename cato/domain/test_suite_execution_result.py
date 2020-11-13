from dataclasses import dataclass

from cato.domain import TestResult
from cato.domain.TestSuite import TestSuite


@dataclass
class TestSuiteExecutionResult:
    test_suite: TestSuite
    result: TestResult
