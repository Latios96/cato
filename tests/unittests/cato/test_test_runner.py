import time
from unittest import mock

from cato.domain.config import Config, RunConfig
from cato.domain.test import Test
from cato.domain.test_status import TestStatus
from cato.domain.test_suite import TestSuite
from cato.image_utils.image_comparator import ImageComparator
from cato.reporter.reporter import Reporter
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.runners.command_runner import CommandRunner, CommandResult
from cato.file_system_abstractions.output_folder import OutputFolder
from cato.runners.test_runner import TestRunner
from cato_server.domain.test_identifier import TestIdentifier
from tests.utils import mock_safe

EXAMPLE_PROJECT = "Example Project"


@mock.patch("cato.runners.test_runner.TestHeartbeatReporter")
def test_should_report_test_start(mock_heartbeat_reporter_class):
    mock_heartbeat_reporter_class.return_value = mock.MagicMock()
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder = mock_safe(OutputFolder)
    image_comparator = mock_safe(ImageComparator)
    image_comparator.compare.return_value = True
    test_execution_reporter = mock_safe(TestExecutionReporter)
    test_runner = TestRunner(
        command_runner,
        reporter,
        output_folder,
        image_comparator,
        test_execution_reporter,
    )
    test = Test(name="my_first_test", command="dummy_command", variables={})
    test_suite = TestSuite(name="suite", tests=[])

    test_runner.run_test(
        RunConfig(
            project_name=EXAMPLE_PROJECT,
            path="test",
            test_suites=[],
            output_folder="output",
        ),
        test_suite,
        test,
    )

    reporter.report_start_test.assert_called_with(test)
    command_runner.run.assert_called_with(test.command)
    output_folder.create_folder("output", test_suite, test)
    time.sleep(1)
    mock_heartbeat_reporter_class.return_value.start_sending_heartbeats_for_test.assert_called_with(
        TestIdentifier("suite", "my_first_test")
    )
    mock_heartbeat_reporter_class.return_value.stop.assert_called_once()


def test_should_replace_placeholder():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder = mock_safe(OutputFolder)
    image_comparator = mock_safe(ImageComparator)
    image_comparator.compare.return_value = True
    test_execution_reporter = mock_safe(TestExecutionReporter)
    test_runner = TestRunner(
        command_runner,
        reporter,
        output_folder,
        image_comparator,
        test_execution_reporter,
    )
    test = Test(
        name="my_first_test",
        command="crayg -s {test_resources}/test.json -o {image_output_png}",
        variables={},
    )

    test_runner.run_test(
        RunConfig(
            project_name=EXAMPLE_PROJECT,
            path="test",
            test_suites=[],
            output_folder="output",
        ),
        TestSuite(name="suite", tests=[]),
        test,
    )

    reporter.report_start_test.assert_called_with(test)
    command_runner.run.assert_called_with(
        "crayg -s test/suite/my_first_test/test.json -o output/result/suite/my_first_test/my_first_test.png",
    )


def test_should_collect_timing_info():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder = mock_safe(OutputFolder)
    image_comparator = mock_safe(ImageComparator)
    image_comparator.compare.return_value = True
    test_execution_reporter = mock_safe(TestExecutionReporter)
    test_runner = TestRunner(
        command_runner,
        reporter,
        output_folder,
        image_comparator,
        test_execution_reporter,
    )
    test = Test(name="my_first_test", command="dummy_command", variables={})

    result = test_runner.run_test(
        RunConfig(
            project_name=EXAMPLE_PROJECT,
            path="test",
            test_suites=[],
            output_folder="output",
        ),
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
    test_execution_reporter = mock_safe(TestExecutionReporter)
    test_runner = TestRunner(
        command_runner,
        reporter,
        output_folder,
        image_comparator,
        test_execution_reporter,
    )
    test = Test(name="my_first_test", command="dummy_command", variables={})
    command_runner.run.return_value = CommandResult("dummy_command", 0, [])

    result = test_runner.run_test(
        RunConfig(
            project_name=EXAMPLE_PROJECT,
            path="test",
            test_suites=[],
            output_folder="output",
        ),
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
    test_execution_reporter = mock_safe(TestExecutionReporter)
    test_runner = TestRunner(
        command_runner,
        reporter,
        output_folder,
        image_comparator,
        test_execution_reporter,
    )
    test = Test(name="my_first_test", command="dummy_command", variables={})
    command_runner.run.return_value = CommandResult("dummy_command", 1, [])

    result = test_runner.run_test(
        RunConfig(
            project_name=EXAMPLE_PROJECT,
            path="test",
            test_suites=[],
            output_folder="output",
        ),
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
    test_execution_reporter = mock_safe(TestExecutionReporter)
    test_runner = TestRunner(
        command_runner,
        reporter,
        output_folder,
        image_comparator,
        test_execution_reporter,
    )
    test = Test(name="my_first_test", command="dummy_command", variables={})
    command_runner.run.return_value = CommandResult("dummy_command", 0, [])

    result = test_runner.run_test(
        RunConfig(
            project_name=EXAMPLE_PROJECT,
            path="test",
            test_suites=[],
            output_folder="output",
        ),
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
    test_execution_reporter = mock_safe(TestExecutionReporter)
    test_runner = TestRunner(
        command_runner,
        reporter,
        output_folder,
        image_comparator,
        test_execution_reporter,
    )
    test = Test(name="my_first_test", command="dummy_command", variables={})
    command_runner.run.return_value = CommandResult("dummy_command", 0, [])

    result = test_runner.run_test(
        RunConfig(
            project_name=EXAMPLE_PROJECT,
            path="test",
            test_suites=[],
            output_folder="output",
        ),
        TestSuite(name="suite", tests=[]),
        test,
    )

    assert result.status == TestStatus.FAILED
    assert result.message.startswith("Reference image")


def test_should_have_failed_with_missing_image_output():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    output_folder = mock_safe(OutputFolder)
    output_folder.image_output_exists.return_value = False
    image_comparator = mock_safe(ImageComparator)
    magic_mock = mock.MagicMock()
    magic_mock.error = True
    image_comparator.compare.return_value = magic_mock
    test_execution_reporter = mock_safe(TestExecutionReporter)
    test_runner = TestRunner(
        command_runner,
        reporter,
        output_folder,
        image_comparator,
        test_execution_reporter,
    )
    test = Test(name="my_first_test", command="dummy_command", variables={})
    command_runner.run.return_value = CommandResult("dummy_command", 0, [])

    result = test_runner.run_test(
        RunConfig(
            project_name=EXAMPLE_PROJECT,
            path="test",
            test_suites=[],
            output_folder="output",
        ),
        TestSuite(name="suite", tests=[]),
        test,
    )

    assert result.status == TestStatus.FAILED
    assert result.message.startswith("No given image output path exists")
