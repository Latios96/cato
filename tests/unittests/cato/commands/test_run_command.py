# no filter
# suite name
# test identifier
import copy
import datetime
import logging
from unittest.mock import call

import pytest

from cato.commands.run_command import RunCommand
from cato.config.config_file_parser import JsonConfigParser
from cato.domain.comparison_settings import ComparisonSettings
from cato.domain.config import RunConfig
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato_common.domain.test_status import TestStatus
from cato.domain.test_suite import TestSuite
from cato.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
    LastRunInformation,
)
from cato.reporter.end_message_generator import EndMessageGenerator
from cato.reporter.reporter import Reporter
from cato.reporter.timing_report_generator import TimingReportGenerator
from cato.reporter.verbose_mode import VerboseMode
from cato.runners.test_suite_runner import TestSuiteRunner
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.test_identifier import TestIdentifier
from tests.utils import mock_safe

TEST = Test(
    name="My_first_test",
    command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
    variables={"frame": "7"},
    comparison_settings=ComparisonSettings.default(),
)
TEST_SUITE = TestSuite(
    name="My_first_test_Suite",
    tests=[TEST],
    variables={"my_var": "from_suite"},
)
CONFIG = RunConfig(
    project_name="EXAMPLE_PROJECT",
    resource_path="test",
    suites=[TEST_SUITE],
    output_folder="output",
    variables={"my_var": "from_config"},
)


@pytest.fixture
def test_context():
    class TestContext:
        def __init__(self):
            self.config = copy.deepcopy(CONFIG)
            self.mock_json_config_parser = mock_safe(JsonConfigParser)
            self.mock_test_suite_runner = mock_safe(TestSuiteRunner)
            self.mock_timing_report_generator = mock_safe(TimingReportGenerator)
            self.mock_end_message_generator = mock_safe(EndMessageGenerator)
            self.mock_logger = mock_safe(logging.Logger)
            self.mock_reporter = mock_safe(Reporter)
            self.mock_last_run_information_repository = mock_safe(
                LastRunInformationRepository
            )
            self.mock_cato_api_client = mock_safe(CatoApiClient)
            self.run_command = RunCommand(
                self.mock_json_config_parser,
                self.mock_test_suite_runner,
                self.mock_timing_report_generator,
                self.mock_end_message_generator,
                self.mock_logger,
                self.mock_reporter,
                lambda x: self.mock_last_run_information_repository,
                self.mock_cato_api_client,
            )
            self.mock_json_config_parser.parse.return_value = self.config
            self.run_command._read_config = lambda x: self.config

    return TestContext()


class TestRunCommand:
    def test_should_run_all_suites_and_tests(self, test_context):
        started_at = datetime.datetime.now()
        finished_at = datetime.datetime.now()
        result = [
            TestSuiteExecutionResult(
                test_suite=TEST_SUITE,
                result=TestStatus.SUCCESS,
                test_results=[
                    TestExecutionResult(
                        test=TEST,
                        status=TestStatus.SUCCESS,
                        output=["this", "is", "my", "output"],
                        seconds=4,
                        message="",
                        image_output=None,
                        reference_image=None,
                        diff_image=None,
                        started_at=started_at,
                        finished_at=finished_at,
                        error_value=1,
                        failure_reason=None,
                    )
                ],
            )
        ]
        test_context.mock_test_suite_runner.run_test_suites.return_value = result
        test_context.mock_timing_report_generator.generate.return_value = (
            "Timing report"
        )
        test_context.mock_end_message_generator.generate_end_message.return_value = (
            "End message"
        )

        test_context.run_command.run("my_path", None, None, False, VerboseMode.DEFAULT)

        test_context.mock_test_suite_runner.run_test_suites.assert_called_with(
            test_context.config
        )
        test_context.mock_timing_report_generator.generate.assert_called_with(result)
        test_context.mock_end_message_generator.generate_end_message.assert_called_with(
            result
        )
        test_context.mock_logger.info.assert_has_calls(
            [call(""), call("Timing report"), call(""), call("End message")]
        )
        test_context.mock_reporter.set_verbose_mode.assert_called_with(
            VerboseMode.DEFAULT
        )

    def test_should_filter_by_suite_name(self, test_context):
        test_context.run_command.run(
            "my_path", "not existing name", None, False, VerboseMode.DEFAULT
        )

        test_context.mock_test_suite_runner.run_test_suites.assert_called_with(
            test_context.config
        )

        assert test_context.config.suites == []

    def test_should_filter_by_test_identifier(self, test_context):
        test_context.run_command.run(
            "my_path", None, "not_existing_suite/test", False, VerboseMode.DEFAULT
        )

        test_context.mock_test_suite_runner.run_test_suites.assert_called_with(
            test_context.config
        )

        assert test_context.config.suites == []

    def test_should_filter_by_invalid_test_identifier_str(self, test_context):
        with pytest.raises(ValueError):
            test_context.run_command.run(
                "my_path", None, "not_existing_suite", False, VerboseMode.DEFAULT
            )

    def test_existing_last_run_information_should_filter_no_tests_executed(
        self, test_context
    ):
        test_context.mock_last_run_information_repository.read_last_run_information.return_value = LastRunInformation(
            last_run_id=2
        )
        test_context.mock_cato_api_client.get_test_results_by_run_id_and_test_status.return_value = (
            []
        )

        test_context.run_command.run("my_path", None, None, True, VerboseMode.DEFAULT)

        test_context.mock_test_suite_runner.run_test_suites.assert_called_with(
            test_context.config
        )
        assert test_context.config.suites == []

    def test_existing_last_run_information_should_filter_one_test_executed(
        self, test_context
    ):
        test_context.mock_last_run_information_repository.read_last_run_information.return_value = LastRunInformation(
            last_run_id=2
        )
        test_context.mock_cato_api_client.get_test_results_by_run_id_and_test_status.return_value = [
            TestIdentifier.from_string("My_first_test_Suite/My_first_test")
        ]

        test_context.run_command.run("my_path", None, None, True, VerboseMode.DEFAULT)

        test_context.mock_test_suite_runner.run_test_suites.assert_called_with(
            test_context.config
        )
        assert test_context.config.suites == [
            TestSuite(
                name="My_first_test_Suite",
                tests=[TEST],
                variables={"my_var": "from_suite"},
            )
        ]

    def test_existing_last_run_information_should_not_use(self, test_context):
        test_context.mock_last_run_information_repository.read_last_run_information.return_value = LastRunInformation(
            last_run_id=2
        )
        test_context.mock_cato_api_client.get_test_results_by_run_id_and_test_status.return_value = [
            TestIdentifier.from_string("My_first_test_Suite/My_first_test")
        ]

        test_context.run_command.run("my_path", None, None, False, VerboseMode.DEFAULT)

        test_context.mock_test_suite_runner.run_test_suites.assert_called_with(
            test_context.config
        )
        assert test_context.config.suites == CONFIG.suites
