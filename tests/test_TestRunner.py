from unittest import mock

from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_result import TestStatus
from cato.domain.test_suite import TestSuite
from cato.image_comparison.image_comparator import ImageComparator
from cato.reporter.reporter import Reporter
from cato.runners.command_runner import CommandRunner, CommandResult
from cato.file_system_abstractions.output_folder import OutputFolder
from cato.runners.test_runner import TestRunner
from tests.utils import mock_safe


def test_should_report_test_start():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder = mock_safe(OutputFolder)
    image_comparator = mock_safe(ImageComparator)
    image_comparator.compare.return_value = True
    test_runner = TestRunner(command_runner, reporter, output_folder, image_comparator)
    test = Test(name="my first test", command="dummy_command", variables={})
    test_suite = TestSuite(name="suite", tests=[])

    test_runner.run_test(
        Config(path="test", test_suites=[], output_folder="output"), test_suite, test
    )

    reporter.report_start_test.assert_called_with(test)
    command_runner.run.assert_called_with(test.command)
    output_folder.create_folder("output", test_suite, test)


def test_should_replace_placeholder():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder = mock_safe(OutputFolder)
    image_comparator = mock_safe(ImageComparator)
    image_comparator.compare.return_value = True
    test_runner = TestRunner(command_runner, reporter, output_folder, image_comparator)
    test = Test(
        name="my first test",
        command="crayg -s {test_resources}/test.json -o {image_output_png}",
        variables={},
    )

    test_runner.run_test(
        Config(path="test", test_suites=[], output_folder="output"),
        TestSuite(name="suite", tests=[]),
        test,
    )

    reporter.report_start_test.assert_called_with(test)
    command_runner.run.assert_called_with(
        "crayg -s test/suite/my first test/test.json -o output/result/suite/my first test/my first test.png",
    )


def test_should_collect_timing_info():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder = mock_safe(OutputFolder)
    image_comparator = mock_safe(ImageComparator)
    image_comparator.compare.return_value = True
    test_runner = TestRunner(command_runner, reporter, output_folder, image_comparator)
    test = Test(name="my first test", command="dummy_command", variables={})

    result = test_runner.run_test(
        Config(path="test", test_suites=[], output_folder="output"),
        TestSuite(name="suite", tests=[]),
        test,
    )

    assert result.seconds >= 0


def test_should_have_succeded_with_exit_code_0():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder = mock_safe(OutputFolder)
    output_folder.image_output_exists.return_value = True
    image_comparator = mock_safe(ImageComparator)
    magic_mock = mock.MagicMock()
    magic_mock.error = False
    image_comparator.compare.return_value = magic_mock
    test_runner = TestRunner(command_runner, reporter, output_folder, image_comparator)
    test = Test(name="my first test", command="dummy_command", variables={})
    command_runner.run.return_value = CommandResult("dummy_command", 0, [])

    result = test_runner.run_test(
        Config(path="test", test_suites=[], output_folder="output"),
        TestSuite(name="suite", tests=[]),
        test,
    )

    assert result.status == TestStatus.SUCCESS


def test_should_have_failed_with_exit_code_0():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder = mock_safe(OutputFolder)
    output_folder.reference_image_exists.return_value = True
    image_comparator = mock_safe(ImageComparator)
    test_runner = TestRunner(command_runner, reporter, output_folder, image_comparator)
    test = Test(name="my first test", command="dummy_command", variables={})
    command_runner.run.return_value = CommandResult("dummy_command", 1, [])

    result = test_runner.run_test(
        Config(path="test", test_suites=[], output_folder="output"),
        TestSuite(name="suite", tests=[]),
        test,
    )

    assert result.status == TestStatus.FAILED


def test_should_have_failed_with_images_not_equal():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder = mock_safe(OutputFolder)
    image_comparator = mock_safe(ImageComparator)
    magic_mock = mock.MagicMock()
    magic_mock.error = True
    image_comparator.compare.return_value = magic_mock

    test_runner = TestRunner(command_runner, reporter, output_folder, image_comparator)
    test = Test(name="my first test", command="dummy_command", variables={})
    command_runner.run.return_value = CommandResult("dummy_command", 0, [])

    result = test_runner.run_test(
        Config(path="test", test_suites=[], output_folder="output"),
        TestSuite(name="suite", tests=[]),
        test,
    )

    assert result.status == TestStatus.FAILED
    assert result.message == "Images are not equal!"


def test_should_have_failed_with_missing_reference_image():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder = mock_safe(OutputFolder)
    output_folder.reference_image_exists.return_value = False
    image_comparator = mock_safe(ImageComparator)
    magic_mock = mock.MagicMock()
    magic_mock.error = True
    image_comparator.compare.return_value = magic_mock

    test_runner = TestRunner(command_runner, reporter, output_folder, image_comparator)
    test = Test(name="my first test", command="dummy_command", variables={})
    command_runner.run.return_value = CommandResult("dummy_command", 0, [])

    result = test_runner.run_test(
        Config(path="test", test_suites=[], output_folder="output"),
        TestSuite(name="suite", tests=[]),
        test,
    )

    assert result.status == TestStatus.FAILED
    assert result.message.startswith("Reference image")
