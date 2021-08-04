from typing import List, Callable

from cato.domain.config import RunConfig
from cato.domain.test_status import TestStatus
from cato.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
)
from cato.reporter.reporter import Reporter
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.runners.test_runner import TestRunner


class TestSuiteRunner:
    __test__ = False

    def __init__(
        self,
        test_runner: TestRunner,
        reporter: Reporter,
        test_execution_reporter: TestExecutionReporter,
        last_run_information_repository_factory: Callable[
            [str], LastRunInformationRepository
        ],
    ):
        self._test_runner = test_runner
        self._reporter = reporter
        self._test_execution_reporter = test_execution_reporter
        self._last_run_information_repository_factory = (
            last_run_information_repository_factory
        )

    def run_test_suites(self, config: RunConfig) -> List[TestSuiteExecutionResult]:

        if not config.suites:
            raise ValueError("At least one TestSuite is required!")

        results = []

        self._test_execution_reporter.start_execution(
            config.project_name, config.suites
        )

        for suite in config.suites:
            test_results = []
            suite_status = TestStatus.SUCCESS
            self._reporter.report_start_test_suite(suite)
            for test in suite.tests:
                self._test_execution_reporter.report_test_execution_start(suite, test)
                result = self._test_runner.run_test(config, suite, test)
                if result.status == TestStatus.SUCCESS:
                    self._reporter.report_test_success(result)
                else:
                    self._reporter.report_test_failure(result)
                    suite_status = TestStatus.FAILED
                test_results.append(result)
                self._test_execution_reporter.report_test_result(suite, result)

            results.append(TestSuiteExecutionResult(suite, suite_status, test_results))

        self._test_execution_reporter.report_test_execution_end(
            self._last_run_information_repository_factory(config.output_folder)
        )

        return results
