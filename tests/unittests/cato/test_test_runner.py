import time
from unittest import mock
from unittest.mock import ANY

from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings
from cato.domain.config import RunConfig
from cato.domain.test import Test
from cato.domain.test_status import TestStatus
from cato.domain.test_suite import TestSuite
from cato.file_system_abstractions.output_folder import OutputFolder
from cato.reporter.reporter import Reporter
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.runners.command_runner import CommandRunner, CommandResult
from cato.runners.test_runner import TestRunner
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.image import Image
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.compare_image_result import CompareImageResult
from tests.utils import mock_safe

EXAMPLE_PROJECT = "Example Project"


class TestTestRunner:
    def _mocked_store_image(self, path):
        self.counter += 1
        return Image(
            id=self.counter,
            name="test",
            original_file_id=1,
            channels=[],
            width=10,
            height=20,
        )

    def setup_method(self):
        self.counter = 0
        self.reporter = mock_safe(Reporter)
        self.command_runner = mock_safe(CommandRunner)
        self.output_folder = mock_safe(OutputFolder)
        self.test_execution_reporter = mock_safe(TestExecutionReporter)
        self.mock_cato_api_client = mock_safe(CatoApiClient)
        self.mock_cato_api_client.upload_image.side_effect = self._mocked_store_image
        self.mock_cato_api_client.compare_images.return_value = CompareImageResult(
            status=TestStatus.SUCCESS,
            message="",
            reference_image_id=1,
            output_image_id=2,
            diff_image_id=3,
            error=1,
        )

    @mock.patch("cato.runners.test_runner.TestHeartbeatReporter")
    def test_should_report_test_start(self, mock_heartbeat_reporter_class):
        mock_heartbeat_reporter_class.return_value = mock.MagicMock()
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            self.test_execution_reporter,
            self.mock_cato_api_client,
        )
        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )
        test_suite = TestSuite(name="suite", tests=[])

        test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
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
            self.test_execution_reporter,
            self.mock_cato_api_client,
        )
        test = Test(
            name="my_first_test",
            command="crayg -s {test_resources}/test.json -o {image_output_png}",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )

        test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
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
            self.test_execution_reporter,
            self.mock_cato_api_client,
        )
        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )

        result = test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.seconds >= 0

    def test_should_have_succeded_with_exit_code_0(
        self,
    ):
        comparison_settings = ComparisonSettings(ComparisonMethod.SSIM, 0.2)
        self.output_folder.image_output_exists.return_value = True
        test_execution_reporter = mock_safe(TestExecutionReporter)
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            test_execution_reporter,
            self.mock_cato_api_client,
        )
        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=comparison_settings,
        )
        self.command_runner.run.return_value = CommandResult("dummy_command", 0, [])

        result = test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == TestStatus.SUCCESS
        assert result.image_output == 2
        assert result.reference_image == 1
        assert result.diff_image == 3
        self.mock_cato_api_client.upload_image.assert_not_called()
        self.mock_cato_api_client.compare_images.assert_called_with(
            ANY, ANY, comparison_settings
        )

    def test_should_have_failed_with_exit_code_0(
        self,
    ):
        self.output_folder.reference_image_exists.return_value = True

        test_execution_reporter = mock_safe(TestExecutionReporter)
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            test_execution_reporter,
            self.mock_cato_api_client,
        )
        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )
        self.command_runner.run.return_value = CommandResult("dummy_command", 1, [])

        result = test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == TestStatus.FAILED

    def test_should_have_failed_with_images_not_equal(
        self,
    ):
        comparison_settings = ComparisonSettings(ComparisonMethod.SSIM, 0.2)
        self.mock_cato_api_client.compare_images.return_value = CompareImageResult(
            status=TestStatus.FAILED,
            message="Images are not equal!",
            reference_image_id=1,
            output_image_id=2,
            diff_image_id=3,
            error=1,
        )
        test_execution_reporter = mock_safe(TestExecutionReporter)
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            test_execution_reporter,
            self.mock_cato_api_client,
        )
        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=comparison_settings,
        )
        self.command_runner.run.return_value = CommandResult("dummy_command", 0, [])

        result = test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == TestStatus.FAILED
        assert result.message == "Images are not equal!"
        assert result.image_output == 1
        assert result.reference_image == 2
        assert result.diff_image == 3
        self.mock_cato_api_client.upload_image.assert_not_called()
        self.mock_cato_api_client.compare_images.assert_called_with(
            ANY, ANY, comparison_settings
        )

    def test_should_have_failed_with_missing_reference_image(
        self,
    ):
        self.output_folder.reference_image_exists.return_value = False
        self.mock_cato_api_client.compare_images.return_value = CompareImageResult(
            status=TestStatus.FAILED,
            message="Images are not equal!",
            reference_image_id=1,
            output_image_id=2,
            diff_image_id=3,
            error=1,
        )
        test_execution_reporter = mock_safe(TestExecutionReporter)
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            test_execution_reporter,
            self.mock_cato_api_client,
        )
        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )
        self.command_runner.run.return_value = CommandResult("dummy_command", 0, [])

        result = test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == TestStatus.FAILED
        assert result.message.startswith("Reference image")
        assert result.image_output == 1
        assert result.reference_image is None
        assert result.diff_image is None
        self.reporter.report_message.assert_called_with(result.message)
        assert self.mock_cato_api_client.upload_image.call_count == 1

    def test_should_have_failed_with_missing_image_output(
        self,
    ):
        self.output_folder.image_output_exists.return_value = False
        self.mock_cato_api_client.compare_images.return_value = CompareImageResult(
            status=TestStatus.FAILED,
            message="Images are not equal!",
            reference_image_id=1,
            output_image_id=2,
            diff_image_id=3,
            error=1,
        )
        test_execution_reporter = mock_safe(TestExecutionReporter)
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            test_execution_reporter,
            self.mock_cato_api_client,
        )
        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )
        self.command_runner.run.return_value = CommandResult("dummy_command", 0, [])

        result = test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == TestStatus.FAILED
        assert result.message.startswith("No given image output path exists")
        assert result.image_output is None
        assert result.reference_image == 1
        assert result.diff_image is None
        self.reporter.report_message.assert_called_with(result.message)
        assert self.mock_cato_api_client.upload_image.call_count == 1

    def test_should_have_failed_with_missing_reference_and_image_output(
        self,
    ):
        self.output_folder.image_output_exists.return_value = False
        self.output_folder.reference_image_exists.return_value = False
        self.mock_cato_api_client.compare_images.return_value = CompareImageResult(
            status=TestStatus.FAILED,
            message="Images are not equal!",
            reference_image_id=1,
            output_image_id=2,
            diff_image_id=3,
            error=1,
        )
        test_execution_reporter = mock_safe(TestExecutionReporter)
        test_runner = TestRunner(
            self.command_runner,
            self.reporter,
            self.output_folder,
            test_execution_reporter,
            self.mock_cato_api_client,
        )
        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )
        self.command_runner.run.return_value = CommandResult("dummy_command", 0, [])

        result = test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == TestStatus.FAILED
        assert result.message.startswith("No given image output path exists")
        assert result.image_output is None
        assert result.reference_image is None
        assert result.diff_image is None
        self.reporter.report_message.assert_any_call(result.message.split(", ")[0])
        self.reporter.report_message.assert_any_call(result.message.split(", ")[1])
        self.mock_cato_api_client.upload_image.assert_not_called()
