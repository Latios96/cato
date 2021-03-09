import datetime
import logging

import pytest

from cato.commands.worker_run_command import WorkerRunCommand
from cato.config.config_encoder import ConfigEncoder
from cato.config.config_file_parser import JsonConfigParser
from cato.config.config_file_writer import ConfigFileWriter
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_status import TestStatus
from cato.reporter.reporter import Reporter
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.runners.test_runner import TestRunner
from tests.utils import mock_safe


class TestWorkerRunCommand:
    def setup_method(self, method):
        self.config_encoder = ConfigEncoder(ConfigFileWriter(), JsonConfigParser())
        self.mock_test_execution_reporter = mock_safe(TestExecutionReporter)
        self.mock_test_runner = mock_safe(TestRunner)
        self.mock_reporter = mock_safe(Reporter)
        self.mock_logger = mock_safe(logging.Logger)
        self.worker_command = WorkerRunCommand(
            self.config_encoder,
            self.mock_test_execution_reporter,
            self.mock_test_runner,
            self.mock_reporter,
            self.mock_logger,
        )

    def test_not_matching_identifier_for_suite_should_raise(self, config_fixture):
        config_str = self.config_encoder.encode(config_fixture.CONFIG)

        with pytest.raises(ValueError):
            self.worker_command.execute(
                config_str.decode(), "test/My_first_test", 5, "some/path"
            )

    def test_not_matching_identifier_for_test_should_raise(self, config_fixture):
        config_str = self.config_encoder.encode(config_fixture.CONFIG)

        with pytest.raises(ValueError):
            self.worker_command.execute(
                config_str.decode(), "My_first_test_Suite/test", 5, "some/path"
            )

    def test_test_run_success(self, config_fixture):
        config_str = self.config_encoder.encode(config_fixture.CONFIG)
        execution_result = TestExecutionResult(
            config_fixture.TEST,
            TestStatus.SUCCESS,
            [],
            1,
            "this is a message",
            None,
            None,
            datetime.datetime.now(),
            datetime.datetime.now(),
        )
        self.mock_test_runner.run_test.return_value = execution_result

        self.worker_command.execute(
            config_str.decode(), "My_first_test_Suite/My_first_test", 5, "some/path"
        )

        self.mock_test_execution_reporter.use_run_id.assert_called_with(5)
        self.mock_test_execution_reporter.report_test_execution_start.assert_called_with(
            config_fixture.TEST_SUITE, config_fixture.TEST
        )
        self.mock_test_runner.run_test.assert_called_once()
        self.mock_reporter.report_test_success.assert_called_once()
        self.mock_logger.info.assert_called_with(
            f"Test My_first_test_Suite/My_first_test passed in f{execution_result.seconds}"
        )

    def test_test_run_failure(self, config_fixture):
        config_str = self.config_encoder.encode(config_fixture.CONFIG)
        execution_result = TestExecutionResult(
            config_fixture.TEST,
            TestStatus.FAILED,
            [],
            1,
            "this is a message",
            None,
            None,
            datetime.datetime.now(),
            datetime.datetime.now(),
        )
        self.mock_test_runner.run_test.return_value = execution_result

        self.worker_command.execute(
            config_str.decode(), "My_first_test_Suite/My_first_test", 5, "some/path"
        )

        self.mock_test_execution_reporter.use_run_id.assert_called_with(5)
        self.mock_test_execution_reporter.report_test_execution_start.assert_called_with(
            config_fixture.TEST_SUITE, config_fixture.TEST
        )
        self.mock_test_runner.run_test.assert_called_once()
        self.mock_reporter.report_test_failure.assert_called_once()
        self.mock_logger.info.assert_called_with(
            f"Test My_first_test_Suite/My_first_test failed in f{execution_result.seconds}: f{execution_result.message}"
        )
