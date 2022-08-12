import pytest

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.config import RunConfig
from cato_common.domain.test import Test
from cato_common.domain.test_execution_result import TestExecutionResult
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.test_suite import TestSuite
from cato_common.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
)
from cato.reporter.reporter import Reporter
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.runners.test_runner import TestRunner
from cato.runners.test_suite_runner import TestSuiteRunner
from cato_common.utils.datetime_utils import aware_now_in_utc
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
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="",
                suites=[],
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
    test = Test(
        name="my_first_test",
        command="dummy_command",
        variables={},
        comparison_settings=ComparisonSettings.default(),
    )
    test_suite = TestSuite(name="example", tests=[test])
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="",
        suites=[test_suite],
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
    test = Test(
        name="my_first_test",
        command="dummy_command",
        variables={},
        comparison_settings=ComparisonSettings.default(),
    )
    test_suite = TestSuite(name="example", tests=[test])
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="",
        suites=[test_suite],
        output_folder="output",
    )
    execution_result = TestExecutionResult(
        test,
        ResultStatus.SUCCESS,
        [],
        1,
        "this is a message",
        None,
        None,
        None,
        aware_now_in_utc(),
        aware_now_in_utc(),
        1,
        failure_reason=None,
    )
    mock_test_runner.run_test.return_value = execution_result

    result = test_suite_runner.run_test_suites(config)

    assert result == [
        TestSuiteExecutionResult(test_suite, ResultStatus.SUCCESS, [execution_result])
    ]
    mock_execution_reporter.report_test_execution_end.assert_called_with(
        mock_last_run_information_repository
    )
