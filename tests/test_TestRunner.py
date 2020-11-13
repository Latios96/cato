import os

from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_result import TestResult
from cato.domain.test_suite import TestSuite
from cato.reporter.reporter import Reporter
from cato.runners.command_runner import CommandRunner, CommandResult
from cato.runners.test_runner import TestRunner
from tests.utils import mock_safe


def test_should_report_test_start():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    test_runner = TestRunner(command_runner, reporter)
    test = Test(name="my first test", command="dummy_command")

    test_runner.run_test(
        Config(path="test", test_suites=[]), TestSuite(name="suite", tests=[]), test
    )

    reporter.report_start_test.assert_called_with(test)
    command_runner.run.assert_called_with(test.command)


def test_should_replace_placeholder():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    test_runner = TestRunner(command_runner, reporter)
    test = Test(
        name="my first test",
        command="crayg -s {test_resources}/test.json -o {image_output_png}",
    )

    test_runner.run_test(
        Config(path="test", test_suites=[]), TestSuite(name="suite", tests=[]), test
    )

    reporter.report_start_test.assert_called_with(test)
    command_runner.run.assert_called_with(
        "crayg -s {}/test.json -o {}".format(
            os.path.join("test", "suite", "my first test"),
            os.path.join("result", "suite", "my first test", "my first test.png"),
        ),
    )


def test_should_collect_timing_info():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    test_runner = TestRunner(command_runner, reporter)
    test = Test(name="my first test", command="dummy_command")

    result = test_runner.run_test(
        Config(path="test", test_suites=[]), TestSuite(name="suite", tests=[]), test
    )

    assert result.seconds >= 0


def test_should_have_succeded_with_exit_code_0():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    test_runner = TestRunner(command_runner, reporter)
    test = Test(name="my first test", command="dummy_command")
    command_runner.run.return_value = CommandResult("dummy_command", 0, [])

    result = test_runner.run_test(
        Config(path="test", test_suites=[]), TestSuite(name="suite", tests=[]), test
    )

    assert result.result == TestResult.SUCCESS


def test_should_have_failed_with_exit_code_0():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    test_runner = TestRunner(command_runner, reporter)
    test = Test(name="my first test", command="dummy_command")
    command_runner.run.return_value = CommandResult("dummy_command", 1, [])

    result = test_runner.run_test(
        Config(path="test", test_suites=[]), TestSuite(name="suite", tests=[]), test
    )

    assert result.result == TestResult.FAILED
