import copy
import logging
import os
import sys

import pytest

from cato.commands.submit_command import SubmitCommand
from cato.config.config_file_parser import JsonConfigParser
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
    LastRunInformation,
)
from cato.reporter.end_message_generator import EndMessageGenerator
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.reporter.timing_report_generator import TimingReportGenerator
from cato.runners.test_suite_runner import TestSuiteRunner
from cato_api_client.cato_api_client import CatoApiClient
from cato_server.domain.test_identifier import TestIdentifier
from cato_server.schedulers.submission_info import SubmissionInfo
from tests.unittests.cato.commands.test_run_command import CONFIG
from tests.utils import mock_safe


class TestSubmitCommand:
    def setup_method(self, method):
        self.config = copy.deepcopy(CONFIG)
        self.mock_json_config_parser = mock_safe(JsonConfigParser)
        self.mock_test_suite_runner = mock_safe(TestSuiteRunner)
        self.mock_timing_report_generator = mock_safe(TimingReportGenerator)
        self.mock_end_message_generator = mock_safe(EndMessageGenerator)
        self.mock_logger = mock_safe(logging.Logger)
        self.mock_test_execution_reporter = mock_safe(TestExecutionReporter)
        self.mock_last_run_information_repository = mock_safe(
            LastRunInformationRepository
        )
        self.mock_cato_api_client = mock_safe(CatoApiClient)
        self.submit_command = SubmitCommand(
            self.mock_json_config_parser,
            self.mock_logger,
            lambda x: self.mock_last_run_information_repository,
            self.mock_cato_api_client,
            self.mock_test_execution_reporter,
        )
        self.mock_json_config_parser.parse.return_value = self.config

    def test_should_submit_all_tests(self):
        self.mock_test_execution_reporter.run_id.return_value = 42

        self.submit_command.run("my_path", None, None, False)

        self.mock_test_execution_reporter.start_execution.assert_called_with(
            self.config.project_name, self.config.test_suites
        )
        self.mock_cato_api_client.submit_to_scheduler.assert_called_with(
            SubmissionInfo(
                config=self.config,
                run_id=42,
                resource_path=os.path.join("test", "config.ini"),
                executable=sys.executable,
            )
        )

    def test_should_raise_value_error_if_no_tests_match_suite_name(self):
        self.mock_test_execution_reporter.run_id.return_value = 42

        with pytest.raises(ValueError):
            self.submit_command.run("my_path", "not existing name", None, False)

    def test_should_raise_value_error_if_no_tests_match_suite_name_test_identifier(
        self,
    ):
        self.mock_test_execution_reporter.run_id.return_value = 42

        with pytest.raises(ValueError):
            self.submit_command.run("my_path", None, "not/existing name", False)

    def test_should_raise_value_error_if_no_tests_match_last_failed(
        self,
    ):
        self.mock_last_run_information_repository.read_last_run_information.return_value = LastRunInformation(
            last_run_id=2
        )
        self.mock_cato_api_client.get_test_results_by_run_id_and_test_status.return_value = [
            TestIdentifier.from_string("My_first_test_Suite/My_first_test")
        ]

        with pytest.raises(ValueError):
            self.submit_command.run("my_path", None, "not/existing name", False)
