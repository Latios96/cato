import time
from unittest import mock
from unittest.mock import Mock

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


class TestTestRunner:
    def setup_method(self):
        self.reporter = mock_safe(Reporter)
        self.command_runner = mock_safe(CommandRunner)
        self.output_folder = mock_safe(OutputFolder)
        self.image_comparator = mock_safe(ImageComparator)
        self.image_comparator.compare.return_value = True
        self.test_execution_reporter = mock_safe(TestExecutionReporter)

    @mock.patch("cato.runners.test_runner.TestHeartbeatReporter")
    def test_should_report_test_start(self, mock_heartbeat_reporter_class):
        mock_heartbeat_reporter_class.return_value = mock.MagicMock()
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            self.image_comparator,
            self.test_execution_reporter,
        )
        test = Test(name="my_first_test", command="dummy_command", variables={})
        test_suite = TestSuite(name="suite", tests=[])

        test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                test_suites=[],
                output_folder="output",
            ),
            test_suite,
            test,
        )

        self.reporter.report_start_test.assert_called_with(test)
        self.command_runner.run.assert_called_with(test.command)
        self.output_folder.create_folder("output", test_suite, test)
        time.sleep(1)
        mock_heartbeat_reporter_class.return_value.start_sending_heartbeats_for_test.assert_called_with(
            TestIdentifier("suite", "my_first_test")
        )
        mock_heartbeat_reporter_class.return_value.stop.assert_called_once()

    def test_should_replace_placeholder(
        self,
    ):
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            self.image_comparator,
            self.test_execution_reporter,
        )
        test = Test(
            name="my_first_test",
            command="crayg -s {test_resources}/test.json -o {image_output_png}",
            variables={},
        )

        test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                test_suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        self.reporter.report_start_test.assert_called_with(test)
        self.command_runner.run.assert_called_with(
            "crayg -s test/suite/my_first_test/test.json -o output/result/suite/my_first_test/my_first_test.png",
        )

    def test_should_collect_timing_info(
        self,
    ):
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            self.image_comparator,
            self.test_execution_reporter,
        )
        test = Test(name="my_first_test", command="dummy_command", variables={})

        result = test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                test_suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.seconds >= 0

    def test_should_have_succeded_with_exit_code_0(
        self,
    ):
        self.output_folder.image_output_exists.return_value = True

        magic_mock = mock.MagicMock()
        magic_mock.error = False
        self.image_comparator.compare.return_value = magic_mock
        test_execution_reporter = mock_safe(TestExecutionReporter)
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            self.image_comparator,
            test_execution_reporter,
        )
        test = Test(name="my_first_test", command="dummy_command", variables={})
        self.command_runner.run.return_value = CommandResult("dummy_command", 0, [])

        result = test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                test_suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == TestStatus.SUCCESS

    def test_should_have_failed_with_exit_code_0(
        self,
    ):
        self.output_folder.reference_image_exists.return_value = True

        test_execution_reporter = mock_safe(TestExecutionReporter)
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            self.image_comparator,
            test_execution_reporter,
        )
        test = Test(name="my_first_test", command="dummy_command", variables={})
        self.command_runner.run.return_value = CommandResult("dummy_command", 1, [])

        result = test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                test_suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == TestStatus.FAILED

    def test_should_have_failed_with_images_not_equal(
        self,
    ):
        magic_mock = mock.MagicMock()
        magic_mock.error = True
        self.image_comparator.compare.return_value = magic_mock
        test_execution_reporter = mock_safe(TestExecutionReporter)
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            self.image_comparator,
            test_execution_reporter,
        )
        test = Test(name="my_first_test", command="dummy_command", variables={})
        self.command_runner.run.return_value = CommandResult("dummy_command", 0, [])

        result = test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                test_suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == TestStatus.FAILED
        assert result.message == "Images are not equal!"

    def test_should_have_failed_with_missing_reference_image(
        self,
    ):
        self.output_folder.reference_image_exists.return_value = False

        magic_mock = mock.MagicMock()
        magic_mock.error = True
        self.image_comparator.compare.return_value = magic_mock
        test_execution_reporter = mock_safe(TestExecutionReporter)
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            self.image_comparator,
            test_execution_reporter,
        )
        test = Test(name="my_first_test", command="dummy_command", variables={})
        self.command_runner.run.return_value = CommandResult("dummy_command", 0, [])

        result = test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                test_suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == TestStatus.FAILED
        assert result.message.startswith("Reference image")
        assert result.image_output is not None
        assert result.reference_image is None
        self.reporter.report_message.assert_called_with(result.message)

    def test_should_have_failed_with_missing_image_output(
        self,
    ):
        self.output_folder.image_output_exists.return_value = False

        magic_mock = mock.MagicMock()
        magic_mock.error = True
        self.image_comparator.compare.return_value = magic_mock
        test_execution_reporter = mock_safe(TestExecutionReporter)
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            self.image_comparator,
            test_execution_reporter,
        )
        test = Test(name="my_first_test", command="dummy_command", variables={})
        self.command_runner.run.return_value = CommandResult("dummy_command", 0, [])

        result = test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                test_suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == TestStatus.FAILED
        assert result.message.startswith("No given image output path exists")
        assert result.image_output is None
        assert result.reference_image is not None
        self.reporter.report_message.assert_called_with(result.message)

    def test_should_have_failed_with_missing_reference_and_image_output(
        self,
    ):
        self.output_folder.image_output_exists.return_value = False
        self.output_folder.reference_image_exists.return_value = False

        magic_mock = mock.MagicMock()
        magic_mock.error = True
        self.image_comparator.compare.return_value = magic_mock
        test_execution_reporter = mock_safe(TestExecutionReporter)
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            self.image_comparator,
            test_execution_reporter,
        )
        test = Test(name="my_first_test", command="dummy_command", variables={})
        self.command_runner.run.return_value = CommandResult("dummy_command", 0, [])

        result = test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                test_suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == TestStatus.FAILED
        assert result.message.startswith("No given image output path exists")
        assert result.image_output is None
        assert result.reference_image is None
        self.reporter.report_message.assert_any_call(result.message.split(", ")[0])
        self.reporter.report_message.assert_any_call(result.message.split(", ")[1])
