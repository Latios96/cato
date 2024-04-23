from typing import List, Callable

from cato.reporter.performance_stats_collector import PerformanceStatsCollector
from cato_common.domain.config import RunConfig
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.test_suite_execution_result import TestSuiteExecutionResult
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
        performance_stats_collector: PerformanceStatsCollector,
    ):
        self._test_runner = test_runner
        self._reporter = reporter
        self._test_execution_reporter = test_execution_reporter
        self._last_run_information_repository_factory = (
            last_run_information_repository_factory
        )
        self._performance_stats_collector = performance_stats_collector

    def run_test_suites(self, config: RunConfig) -> List[TestSuiteExecutionResult]:
        if not config.suites:
            raise ValueError("At least one TestSuite is required!")

        results = []
        with self._performance_stats_collector.collect_cato_run_timing():
            with self._performance_stats_collector.collect_create_run_timing():
                self._test_execution_reporter.start_execution(config)

            for suite in config.suites:
                with self._performance_stats_collector.collect_suite_timing(suite.name):
                    test_results = []
                    suite_status = ResultStatus.SUCCESS
                    self._reporter.report_start_test_suite(suite)
                    for test in suite.tests:
                        test_identifier = TestIdentifier(suite.name, test.name)
                        with self._performance_stats_collector.collect_test_timing(
                            test_identifier
                        ):
                            with self._performance_stats_collector.collect_start_test_request_timing():
                                self._test_execution_reporter.report_test_execution_start(
                                    suite, test
                                )

                            result = self._test_runner.run_test(config, suite, test)

                            if result.status == ResultStatus.SUCCESS:
                                self._reporter.report_test_success(result)
                            else:
                                self._reporter.report_test_failure(result)
                                suite_status = ResultStatus.FAILED
                            test_results.append(result)
                            with self._performance_stats_collector.collect_report_test_result():
                                self._test_execution_reporter.report_test_result(
                                    suite, result
                                )

                    results.append(
                        TestSuiteExecutionResult(suite, suite_status, test_results)
                    )

            self._test_execution_reporter.report_test_execution_end(
                self._last_run_information_repository_factory(config.output_folder)
            )

        return results
