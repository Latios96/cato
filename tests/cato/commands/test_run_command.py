# no filter
# suite name
# test identifier
import copy
import datetime

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
from cato.reporter.timing_report_generator import TimingReportGenerator
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


def test_should_run_all_suites_and_tests():
    config = copy.deepcopy(CONFIG)
    mock_json_config_parser = mock_safe(JsonConfigParser)
    mock_test_suite_runner = mock_safe(TestSuiteRunner)
    mock_timing_report_generator = mock_safe(TimingReportGenerator)
    mock_end_message_generator = mock_safe(EndMessageGenerator)
    run_command = RunCommand(
        mock_json_config_parser,
        mock_test_suite_runner,
        mock_timing_report_generator,
        mock_end_message_generator,
    )
    mock_json_config_parser.parse.return_value = config
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
    mock_test_suite_runner.run_test_suites.return_value = result

    run_command.run("my_path", None, None)

    mock_test_suite_runner.run_test_suites.assert_called_with(config)
    mock_timing_report_generator.generate.assert_called_with(result)
    mock_end_message_generator.generate_end_message.assert_called_with(result)


def test_should_filter_by_suite_name():
    config = copy.deepcopy(CONFIG)
    mock_json_config_parser = mock_safe(JsonConfigParser)
    mock_test_suite_runner = mock_safe(TestSuiteRunner)
    mock_timing_report_generator = mock_safe(TimingReportGenerator)
    mock_end_message_generator = mock_safe(EndMessageGenerator)
    run_command = RunCommand(
        mock_json_config_parser,
        mock_test_suite_runner,
        mock_timing_report_generator,
        mock_end_message_generator,
    )
    mock_json_config_parser.parse.return_value = config

    run_command.run("my_path", "not existing name", None)

    mock_test_suite_runner.run_test_suites.assert_called_with(config)

    assert config.test_suites == []


def test_should_filter_by_test_identifier():
    config = copy.deepcopy(CONFIG)
    mock_json_config_parser = mock_safe(JsonConfigParser)
    mock_test_suite_runner = mock_safe(TestSuiteRunner)
    mock_timing_report_generator = mock_safe(TimingReportGenerator)
    mock_end_message_generator = mock_safe(EndMessageGenerator)
    run_command = RunCommand(
        mock_json_config_parser,
        mock_test_suite_runner,
        mock_timing_report_generator,
        mock_end_message_generator,
    )
    mock_json_config_parser.parse.return_value = config

    run_command.run("my_path", None, "not_existing_suite/test")

    mock_test_suite_runner.run_test_suites.assert_called_with(config)

    assert config.test_suites == []


def test_should_filter_by_invalid_test_identifier_str():
    config = copy.deepcopy(CONFIG)
    mock_json_config_parser = mock_safe(JsonConfigParser)
    mock_test_suite_runner = mock_safe(TestSuiteRunner)
    mock_timing_report_generator = mock_safe(TimingReportGenerator)
    mock_end_message_generator = mock_safe(EndMessageGenerator)
    run_command = RunCommand(
        mock_json_config_parser,
        mock_test_suite_runner,
        mock_timing_report_generator,
        mock_end_message_generator,
    )
    mock_json_config_parser.parse.return_value = config

    with pytest.raises(ValueError):
        run_command.run("my_path", None, "not_existing_suite")
