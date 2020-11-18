from typing import List

from cato.domain.config import Config
from cato.domain.test_result import TestStatus
from cato.domain.test_suite import TestSuite
from cato.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.reporter.reporter import Reporter
from cato.runners.test_runner import TestRunner


class TestSuiteRunner:
    def __init__(self, test_runner: TestRunner, reporter: Reporter):
        self._test_runner = test_runner
        self._reporter = reporter

    def run_test_suites(self, config: Config) -> List[TestSuiteExecutionResult]:

        if not config.test_suites:
            raise ValueError("At least one TestSuite is required!")

        results = []

        for suite in config.test_suites:
            test_results = []
            suite_status = TestStatus.SUCCESS
            self._reporter.report_start_test_suite(suite)
            for test in suite.tests:
                result = self._test_runner.run_test(config, suite, test)
                if result.status == TestStatus.SUCCESS:
                    self._reporter.report_test_sucess(result)
                else:
                    self._reporter.report_test_failure(result)
                    suite_status = TestStatus.FAILED
                test_results.append(result)

            results.append(TestSuiteExecutionResult(suite, suite_status, test_results))

        return results
