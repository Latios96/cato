import datetime
import logging

import pytest

from cato.commands.worker_run_command import WorkerRunCommand
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_status import TestStatus
from cato.reporter.reporter import Reporter
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.reporter.verbose_mode import VerboseMode
from cato.runners.test_runner import TestRunner
from cato_api_client.cato_api_client import CatoApiClient
from cato_server.domain.submission_info import SubmissionInfo
from tests.utils import mock_safe


@pytest.fixture()
def submission_info_fixture(config_fixture):
    return SubmissionInfo(
        id=1,
        config=config_fixture.CONFIG,
        run_id=5,
        resource_path="resource_path",
        executable="executable",
    )


class TestWorkerRunCommand:
    def setup_method(self, method):
        self.mock_test_execution_reporter = mock_safe(TestExecutionReporter)
        self.mock_test_runner = mock_safe(TestRunner)
        self.mock_reporter = mock_safe(Reporter)
        self.mock_logger = mock_safe(logging.Logger)
        self.cato_api_client = mock_safe(CatoApiClient)
        self.worker_command = WorkerRunCommand(
            self.mock_test_execution_reporter,
            self.mock_test_runner,
            self.mock_reporter,
            self.mock_logger,
            self.cato_api_client,
        )

    def test_not_matching_identifier_for_suite_should_raise(
        self, submission_info_fixture
    ):
        self.cato_api_client.get_submission_info_by_id.return_value = (
            submission_info_fixture
        )

        with pytest.raises(ValueError):
            self.worker_command.execute(1, "test/My_first_test")

    def test_not_matching_identifier_for_test_should_raise(
        self, submission_info_fixture
    ):
        self.cato_api_client.get_submission_info_by_id.return_value = (
            submission_info_fixture
        )

        with pytest.raises(ValueError):
            self.worker_command.execute(1, "My_first_test_Suite/test")

    def test_test_run_success(self, config_fixture, submission_info_fixture):
        self.cato_api_client.get_submission_info_by_id.return_value = (
            submission_info_fixture
        )
        execution_result = TestExecutionResult(
            config_fixture.TEST,
            TestStatus.SUCCESS,
            [],
            1,
            "this is a message",
            None,
            None,
            None,
            datetime.datetime.now(),
            datetime.datetime.now(),
        )
        self.mock_test_runner.run_test.return_value = execution_result

        self.worker_command.execute(1, "My_first_test_Suite/My_first_test")

        self.mock_test_execution_reporter.use_run_id.assert_called_with(5)
        self.mock_test_execution_reporter.report_test_execution_start.assert_called_with(
            config_fixture.TEST_SUITE, config_fixture.TEST
        )
        self.mock_reporter.set_verbose_mode.assert_called_with(VerboseMode.VERY_VERBOSE)
        self.mock_test_runner.run_test.assert_called_once()
        self.mock_reporter.report_test_success.assert_called_once()

    def test_test_run_failure(self, config_fixture, submission_info_fixture):
        self.cato_api_client.get_submission_info_by_id.return_value = (
            submission_info_fixture
        )
        execution_result = TestExecutionResult(
            config_fixture.TEST,
            TestStatus.FAILED,
            [],
            1,
            "this is a message",
            None,
            None,
            None,
            datetime.datetime.now(),
            datetime.datetime.now(),
        )
        self.mock_test_runner.run_test.return_value = execution_result

        self.worker_command.execute(1, "My_first_test_Suite/My_first_test")

        self.mock_test_execution_reporter.use_run_id.assert_called_with(5)
        self.mock_test_execution_reporter.report_test_execution_start.assert_called_with(
            config_fixture.TEST_SUITE, config_fixture.TEST
        )
        self.mock_test_runner.run_test.assert_called_once()
        self.mock_reporter.report_test_failure.assert_called_once()
