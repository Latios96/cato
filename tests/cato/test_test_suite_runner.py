import datetime

import pytest

from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_status import TestStatus
from cato.domain.test_suite import TestSuite
from cato.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
    LastRunInformation,
)
from cato.reporter.reporter import Reporter
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.runners.test_runner import TestRunner
from cato.runners.test_suite_runner import TestSuiteRunner
from tests.utils import mock_safe

EXAMPLE_PROJECT = "Example project"


def test_run_empty_suites_should_fail():
    mock_reporter = mock_safe(Reporter)
    mock_test_runner = mock_safe(TestRunner)
    mock_execution_reporter = mock_safe(TestExecutionReporter)
    mock_last_run_information_repository = mock_safe(LastRunInformationRepository)
    test_suite_runner = TestSuiteRunner(
        mock_test_runner,
        mock_reporter,
        mock_execution_reporter,
        lambda x: mock_last_run_information_repository,
    )

    with pytest.raises(ValueError):
        test_suite_runner.run_test_suites(
            Config(
                project_name=EXAMPLE_PROJECT,
                path="",
                test_suites=[],
                output_folder="output",
            )
        )


def test_run_suite_should_report_start_and_delegate_to_test_runner():
    mock_reporter = mock_safe(Reporter)
    mock_test_runner = mock_safe(TestRunner)
    mock_execution_reporter = mock_safe(TestExecutionReporter)
    mock_last_run_information_repository = mock_safe(LastRunInformationRepository)
    test_suite_runner = TestSuiteRunner(
        mock_test_runner,
        mock_reporter,
        mock_execution_reporter,
        lambda x: mock_last_run_information_repository,
    )
    test = Test(name="my_first_test", command="dummy_command", variables={})
    test_suite = TestSuite(name="example", tests=[test])
    config = Config(
        project_name=EXAMPLE_PROJECT,
        path="",
        test_suites=[test_suite],
        output_folder="output",
    )

    test_suite_runner.run_test_suites(config)

    mock_reporter.report_start_test_suite.assert_called_once()
    mock_test_runner.run_test.assert_called_with(config, test_suite, test)
    mock_execution_reporter.report_test_execution_end.assert_called_with(
        mock_last_run_information_repository
    )


def test_run_suite_should_return_correctly_collected_results():
    mock_reporter = mock_safe(Reporter)
    mock_test_runner = mock_safe(TestRunner)
    mock_execution_reporter = mock_safe(TestExecutionReporter)
    mock_last_run_information_repository = mock_safe(LastRunInformationRepository)
    test_suite_runner = TestSuiteRunner(
        mock_test_runner,
        mock_reporter,
        mock_execution_reporter,
        lambda x: mock_last_run_information_repository,
    )
    test = Test(name="my_first_test", command="dummy_command", variables={})
    test_suite = TestSuite(name="example", tests=[test])
    config = Config(
        project_name=EXAMPLE_PROJECT,
        path="",
        test_suites=[test_suite],
        output_folder="output",
    )
    execution_result = TestExecutionResult(
        test,
        TestStatus.SUCCESS,
        [],
        1,
        "this is a message",
        None,
        None,
        datetime.datetime.now(),
        datetime.datetime.now(),
    )
    mock_test_runner.run_test.return_value = execution_result

    result = test_suite_runner.run_test_suites(config)

    assert result == [
        TestSuiteExecutionResult(test_suite, TestStatus.SUCCESS, [execution_result])
    ]
    mock_execution_reporter.report_test_execution_end.assert_called_with(
        mock_last_run_information_repository
    )
