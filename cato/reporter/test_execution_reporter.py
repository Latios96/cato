from typing import List

from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_suite import TestSuite


class TestExecutionReporter:
    def start_execution(self, project_name: str, test_suites: List[TestSuite]):
        raise NotImplementedError()

    def report_test_execution_start(self, current_suite: TestSuite, test: Test):
        raise NotImplementedError()

    def report_test_result(
        self, current_suite: TestSuite, test_execution_result: TestExecutionResult
    ):
        raise NotImplementedError()
