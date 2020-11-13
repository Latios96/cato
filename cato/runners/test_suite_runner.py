from typing import List

from cato.domain.test_suite import TestSuite
from cato.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.reporter.reporter import Reporter
from cato.runners.test_runner import TestRunner


class TestSuiteRunner:
    def __init__(self, test_runner: TestRunner, reporter: Reporter):
        self._test_runner = test_runner
        self._reporter = reporter

    def run_test_suites(
        self, test_suites: List[TestSuite]
    ) -> List[TestSuiteExecutionResult]:

        if not test_suites:
            raise ValueError("At least one TestSuite is required!")

        for suite in test_suites:
            self._reporter.report_start_test_suite(suite)
            for test in suite.tests:
                self._test_runner.run_test(test)
        return []
