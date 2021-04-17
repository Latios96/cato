import logging
import os

from cato.commands.base_command import BaseCliCommand
from cato.config.config_encoder import ConfigEncoder
from cato.domain.config import Config, RunConfig
from cato.domain.test import Test
from cato.domain.test_status import TestStatus
from cato.domain.test_suite import filter_by_test_identifier, TestSuite
from cato.reporter.reporter import Reporter
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.reporter.verbose_mode import VerboseMode
from cato.runners.test_runner import TestRunner
from cato_api_client.cato_api_client import CatoApiClient
from cato_server.domain.test_identifier import TestIdentifier


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
    ):
        self._reporter.set_verbose_mode(VerboseMode.VERY_VERBOSE)
        submission_info = self._cato_api_client.get_submission_info_by_id(
            submission_info_id
        )
        if not submission_info:
            raise ValueError("Invalid submission info id: {}".format(submission_info))
        config = submission_info.config

        config.test_suites = filter_by_test_identifier(
            config.test_suites, TestIdentifier.from_string(test_identifier_str)
        )

        if len(config.test_suites) == 0 or len(config.test_suites[0].tests) == 0:
            raise ValueError(
                f"Filter {test_identifier_str} did match not match a test!"
            )

        suite = config.test_suites[0]
        test = config.test_suites[0].tests[0]

        self._test_execution_reporter.use_run_id(submission_info.run_id)

        run_config = RunConfig.from_config(
            config,
            submission_info.resource_path,
            os.path.join(submission_info.resource_path, "output"),
        )  # todo use temporary folder for output
        self._execute_test(run_config, suite, test)

    def _execute_test(self, config: RunConfig, suite: TestSuite, test: Test):
        self._test_execution_reporter.report_test_execution_start(suite, test)

        result = self._test_runner.run_test(config, suite, test)

        if result.status == TestStatus.SUCCESS:
            self._reporter.report_test_success(result)
        else:
            self._reporter.report_test_failure(result)

        self._test_execution_reporter.report_test_result(suite, result)

        self._logger.info("Done.")
