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
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.submission_info import SubmissionInfo
from cato_common.domain.test_identifier import TestIdentifier
from tests.unittests.cato.commands.test_run_command import CONFIG
from tests.utils import mock_safe


@pytest.fixture
def test_context():
    class TestContext:
        def __init__(self):
            self.config = copy.deepcopy(CONFIG)
            self.mock_json_config_parser = mock_safe(JsonConfigParser)
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
            self.submit_command._read_config = lambda x: self.config

    return TestContext()


class TestSubmitCommand:
    def test_should_submit_all_tests(self, test_context):
        test_context.mock_test_execution_reporter.run_id.return_value = 42

        test_context.submit_command.run("my_path", None, None, False)

        test_context.mock_test_execution_reporter.start_execution.assert_called_with(
            test_context.config.project_name, test_context.config.suites
        )
        test_context.mock_logger.info.assert_any_call("Submitting to scheduler..")
        test_context.mock_cato_api_client.submit_to_scheduler.assert_called_with(
            SubmissionInfo(
                id=0,
                config=test_context.config.to_config(),
                run_id=42,
                resource_path=os.path.join("test"),
                executable=sys.executable,
            )
        )
        test_context.mock_logger.info.assert_called_with(
            f"Submitted 1 suite with 1 test to scheduler."
        )

    def test_should_raise_value_error_if_no_tests_match_suite_name(self, test_context):
        test_context.mock_test_execution_reporter.run_id.return_value = 42

        with pytest.raises(ValueError):
            test_context.submit_command.run("my_path", "not existing name", None, False)

    def test_should_raise_value_error_if_no_tests_match_suite_name_test_identifier(
        self, test_context
    ):
        test_context.mock_test_execution_reporter.run_id.return_value = 42

        with pytest.raises(ValueError):
            test_context.submit_command.run("my_path", None, "not/existing name", False)

    def test_should_raise_value_error_if_no_tests_match_last_failed(self, test_context):
        test_context.mock_last_run_information_repository.read_last_run_information.return_value = LastRunInformation(
            last_run_id=2
        )
        test_context.mock_cato_api_client.get_test_results_by_run_id_and_test_status.return_value = [
            TestIdentifier.from_string("My_first_test_Suite/My_first_test")
        ]

        with pytest.raises(ValueError):
            test_context.submit_command.run("my_path", None, "not/existing name", False)
