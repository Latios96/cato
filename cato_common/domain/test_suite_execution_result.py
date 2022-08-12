from dataclasses import dataclass
from typing import List

from cato_common.domain.test_execution_result import TestExecutionResult
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.test_suite import TestSuite


@dataclass
class TestSuiteExecutionResult:
    test_suite: TestSuite
    result: ResultStatus
    test_results: List[TestExecutionResult]

    __test__ = False
