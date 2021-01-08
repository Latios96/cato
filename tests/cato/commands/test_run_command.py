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
from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_status import TestStatus
from cato.domain.test_suite import TestSuite
from cato.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.reporter.end_message_generator import EndMessageGenerator
from cato.reporter.reporter import Reporter
from cato.reporter.timing_report_generator import TimingReportGenerator
from cato.reporter.verbose_mode import VerboseMode
from cato.runners.test_suite_runner import TestSuiteRunner
from tests.utils import mock_safe

TEST = Test(
    name="My_first_test",
    command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
    variables={"frame": "7"},
)
TEST_SUITE = TestSuite(
    name="My_first_test_Suite",
    tests=[TEST],
    variables={"my_var": "from_suite"},
)
CONFIG = Config(
    project_name="EXAMPLE_PROJECT",
    path="test",
    test_suites=[TEST_SUITE],
    output_folder="output",
    variables={"my_var": "from_config"},
)


class TestRunCommand:
    def setup_method(self, method):
        self.config = copy.deepcopy(CONFIG)
        self.mock_json_config_parser = mock_safe(JsonConfigParser)
        self.mock_test_suite_runner = mock_safe(TestSuiteRunner)
        self.mock_timing_report_generator = mock_safe(TimingReportGenerator)
        self.mock_end_message_generator = mock_safe(EndMessageGenerator)
        self.mock_logger = mock_safe(logging.Logger)
        self.mock_reporter = mock_safe(Reporter)
        self.run_command = RunCommand(
            self.mock_json_config_parser,
            self.mock_test_suite_runner,
            self.mock_timing_report_generator,
            self.mock_end_message_generator,
            self.mock_logger,
            self.mock_reporter,
        )
        self.mock_json_config_parser.parse.return_value = self.config

    def test_should_run_all_suites_and_tests(self):
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
                        started_at=started_at,
                        finished_at=finished_at,
                    )
                ],
            )
        ]
        self.mock_test_suite_runner.run_test_suites.return_value = result
        self.mock_timing_report_generator.generate.return_value = "Timing report"
        self.mock_end_message_generator.generate_end_message.return_value = (
            "End message"
        )

        self.run_command.run("my_path", None, None, VerboseMode.DEFAULT)

        self.mock_test_suite_runner.run_test_suites.assert_called_with(self.config)
        self.mock_timing_report_generator.generate.assert_called_with(result)
        self.mock_end_message_generator.generate_end_message.assert_called_with(result)
        self.mock_logger.info.assert_has_calls(
            [call(""), call("Timing report"), call(""), call("End message")]
        )
        self.mock_reporter.set_verbose_mode.assert_called_with(VerboseMode.DEFAULT)

    def test_should_filter_by_suite_name(self):
        self.run_command.run("my_path", "not existing name", None, VerboseMode.DEFAULT)

        self.mock_test_suite_runner.run_test_suites.assert_called_with(self.config)

        assert self.config.test_suites == []

    def test_should_filter_by_test_identifier(self):
        self.run_command.run(
            "my_path", None, "not_existing_suite/test", VerboseMode.DEFAULT
        )

        self.mock_test_suite_runner.run_test_suites.assert_called_with(self.config)

        assert self.config.test_suites == []

    def test_should_filter_by_invalid_test_identifier_str(self):
        with pytest.raises(ValueError):
            self.run_command.run(
                "my_path", None, "not_existing_suite", VerboseMode.DEFAULT
            )
