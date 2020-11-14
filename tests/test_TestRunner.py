import os

from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_result import TestStatus
from cato.domain.test_suite import TestSuite
from cato.reporter.reporter import Reporter
from cato.runners.command_runner import CommandRunner, CommandResult
from cato.runners.output_folder_creator import OutputFolder
from cato.runners.test_runner import TestRunner
from tests.utils import mock_safe


def test_should_report_test_start():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder_creator = mock_safe(OutputFolder)
    test_runner = TestRunner(command_runner, reporter, output_folder_creator)
    test = Test(name="my first test", command="dummy_command",variables={})
    test_suite = TestSuite(name="suite", tests=[])

    test_runner.run_test(
        Config(path="test", test_suites=[], output_folder="output"), test_suite, test
    )

    reporter.report_start_test.assert_called_with(test)
    command_runner.run.assert_called_with(test.command)
    output_folder_creator.create_folder("output", test_suite, test)


def test_should_replace_placeholder():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder_creator = mock_safe(OutputFolder)
    test_runner = TestRunner(command_runner, reporter, output_folder_creator)
    test = Test(
        name="my first test",
        command="crayg -s {test_resources}/test.json -o {image_output_png}"
        , variables={}
    )

    test_runner.run_test(
        Config(path="test", test_suites=[], output_folder="output"),
        TestSuite(name="suite", tests=[]),
        test,
    )

    reporter.report_start_test.assert_called_with(test)
    command_runner.run.assert_called_with(
        "crayg -s test/suite/my first test/test.json -o test/suite/my first test/suite/my first test/my first test.png",
    )


def test_should_collect_timing_info():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder_creator = mock_safe(OutputFolder)
    test_runner = TestRunner(command_runner, reporter, output_folder_creator)
    test = Test(name="my first test", command="dummy_command",variables={})

    result = test_runner.run_test(
        Config(path="test", test_suites=[], output_folder="output"),
        TestSuite(name="suite", tests=[]),
        test,
    )

    assert result.seconds >= 0


def test_should_have_succeded_with_exit_code_0():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder_creator = mock_safe(OutputFolder)
    test_runner = TestRunner(command_runner, reporter, output_folder_creator)
    test = Test(name="my first test", command="dummy_command",variables={})
    command_runner.run.return_value = CommandResult("dummy_command", 0, [])

    result = test_runner.run_test(
        Config(path="test", test_suites=[], output_folder="output"),
        TestSuite(name="suite", tests=[]),
        test,
    )

    assert result.result == TestStatus.SUCCESS


def test_should_have_failed_with_exit_code_0():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder_creator = mock_safe(OutputFolder)
    test_runner = TestRunner(command_runner, reporter, output_folder_creator)
    test = Test(name="my first test", command="dummy_command",variables={})
    command_runner.run.return_value = CommandResult("dummy_command", 1, [])

    result = test_runner.run_test(
        Config(path="test", test_suites=[], output_folder="output"),
        TestSuite(name="suite", tests=[]),
        test,
    )

    assert result.result == TestStatus.FAILED
