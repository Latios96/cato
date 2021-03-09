import logging
import os

from cato.commands.base_command import BaseCliCommand
from cato.config.config_encoder import ConfigEncoder
from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_status import TestStatus
from cato.domain.test_suite import filter_by_test_identifier, TestSuite
from cato.reporter.reporter import Reporter
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.runners.test_runner import TestRunner
from cato_server.domain.test_identifier import TestIdentifier


class WorkerRunCommand(BaseCliCommand):
    def __init__(
        self,
        config_encoder: ConfigEncoder,
        test_execution_reporter: TestExecutionReporter,
        test_runner: TestRunner,
        reporter: Reporter,
        logger: logging.Logger,
    ):
        self._config_encoder = config_encoder
        self._test_execution_reporter = test_execution_reporter
        self._test_runner = test_runner
        self._reporter = reporter
        self._logger = logger

    def execute(
        self,
        encoded_config: str,
        test_identifier_str: str,
        run_id: int,
        resource_path: str,
    ):
        if os.path.isdir(resource_path):
            resource_path = os.path.join("config.ini")
        config = self._config_encoder.decode(encoded_config.encode(), resource_path)

        config.test_suites = filter_by_test_identifier(
            config.test_suites, TestIdentifier.from_string(test_identifier_str)
        )

        if len(config.test_suites) == 0 or len(config.test_suites[0].tests) == 0:
            raise ValueError(
                f"Filter {test_identifier_str} did match not match a test!"
            )

        suite = config.test_suites[0]
        test = config.test_suites[0].tests[0]

        self._test_execution_reporter.use_run_id(run_id)

        self._execute_test(config, suite, test)

    def _execute_test(self, config: Config, suite: TestSuite, test: Test):
        test_identifier = TestIdentifier(suite.name, test.name)

        self._test_execution_reporter.report_test_execution_start(suite, test)

        result = self._test_runner.run_test(config, suite, test)

        if result.status == TestStatus.SUCCESS:
            self._reporter.report_test_success(result)
            self._success_message(test_identifier, result)
        else:
            self._reporter.report_test_failure(result)
            self._failure_message(test_identifier, result)

        self._test_execution_reporter.report_test_result(suite, result)

    def _success_message(
        self, test_identifier: TestIdentifier, result: TestExecutionResult
    ):
        self._logger.info("")
        self._logger.info(f"Test {test_identifier} passed in f{result.seconds}")

    def _failure_message(
        self, test_identifier: TestIdentifier, result: TestExecutionResult
    ):
        self._logger.info("")
        self._logger.info(
            f"Test {test_identifier} failed in f{result.seconds}: f{result.message}"
        )
