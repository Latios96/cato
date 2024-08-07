import logging
import os

from cato.commands.base_command import BaseCliCommand
from cato_common.domain.config import RunConfig
from cato_common.domain.test import Test
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.test_suite import filter_by_test_identifier, TestSuite
from cato.reporter.reporter import Reporter
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.reporter.verbose_mode import VerboseMode
from cato.runners.test_runner import TestRunner
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.test_identifier import TestIdentifier


class WorkerRunCommand(BaseCliCommand):
    def __init__(
        self,
        test_execution_reporter: TestExecutionReporter,
        test_runner: TestRunner,
        reporter: Reporter,
        logger: logging.Logger,
        cato_api_client: CatoApiClient,
    ):
        self._test_execution_reporter = test_execution_reporter
        self._test_runner = test_runner
        self._reporter = reporter
        self._logger = logger
        self._cato_api_client = cato_api_client

    def execute(
        self,
        submission_info_id: int,
        test_identifier_str: str,
    ) -> None:
        self._reporter.set_verbose_mode(VerboseMode.VERY_VERBOSE)
        submission_info = self._cato_api_client.get_submission_info_by_id(
            submission_info_id
        )
        if not submission_info:
            raise ValueError("Invalid submission info id: {}".format(submission_info))
        config = submission_info.config

        config.suites = filter_by_test_identifier(
            config.suites, TestIdentifier.from_string(test_identifier_str)
        )

        if len(config.suites) == 0 or len(config.suites[0].tests) == 0:
            raise ValueError(
                f"Filter {test_identifier_str} did match not match a test!"
            )

        suite = config.suites[0]
        test = config.suites[0].tests[0]

        self._test_execution_reporter.use_run_id(submission_info.run_id)

        run_config = RunConfig.from_config(
            config,
            submission_info.resource_path,
            os.path.join(submission_info.resource_path, "output"),
        )  # todo use temporary folder for output
        self._execute_test(run_config, suite, test)

    def _execute_test(self, config: RunConfig, suite: TestSuite, test: Test) -> None:
        self._test_execution_reporter.report_test_execution_start(suite, test)

        result = self._test_runner.run_test(config, suite, test)

        if result.status == ResultStatus.SUCCESS:
            self._reporter.report_test_success(result)
        else:
            self._reporter.report_test_failure(result)

        self._test_execution_reporter.report_test_result(suite, result)

        self._logger.info("Done.")
