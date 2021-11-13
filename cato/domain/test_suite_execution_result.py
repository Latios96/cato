from dataclasses import dataclass
from typing import List

from cato.domain.test_execution_result import TestExecutionResult
from cato_common.domain.test_status import TestStatus
from cato.domain.test_suite import TestSuite


@dataclass
class TestSuiteExecutionResult:
    test_suite: TestSuite
    result: TestStatus
    test_results: List[TestExecutionResult]

    __test__ = False
