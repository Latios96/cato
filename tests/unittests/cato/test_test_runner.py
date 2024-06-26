import time
from unittest import mock
from unittest.mock import ANY

import pytest

from cato.reporter.performance_stats_collector import PerformanceStatsCollector
from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_result import ComparisonResult
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.config import RunConfig
from cato_common.domain.test import Test
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.test_suite import TestSuite
from cato.file_system_abstractions.output_folder import OutputFolder
from cato.reporter.reporter import Reporter
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.runners.command_runner import CommandRunner, CommandResult
from cato.runners.test_runner import TestRunner
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.image import Image, ImageTranscodingState
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.compare_image_result import CompareImageResult
from cato_common.images.image_comparators.image_comparator import ImageComparator
from tests.utils import mock_safe

EXAMPLE_PROJECT = "Example Project"


@pytest.fixture
def test_context():
    class TestContext:
        def __init__(self):
            self.counter = 0
            self.reporter = mock_safe(Reporter)
            self.command_runner = mock_safe(CommandRunner)
            self.output_folder = mock_safe(OutputFolder)
            self.test_execution_reporter = mock_safe(TestExecutionReporter)
            self.mock_cato_api_client = mock_safe(CatoApiClient)
            self.mock_cato_api_client.upload_image.side_effect = (
                self._mocked_store_image
            )
            self.mock_cato_api_client.upload_image.side_effect = (
                self._mocked_store_image
            )
            self.mock_image_comparator = mock_safe(ImageComparator)
            self.mock_image_comparator.compare.return_value = ComparisonResult(
                status=ResultStatus.SUCCESS,
                message="",
                diff_image="diff-image-path.png",
                error=1,
            )
            self.performance_stats_collector = PerformanceStatsCollector()
            self.test_runner = TestRunner(
                self.command_runner,
                self.reporter,
                self.output_folder,
                self.test_execution_reporter,
                self.mock_cato_api_client,
                self.mock_image_comparator,
                self.performance_stats_collector,
            )

        def _mocked_store_image(self, path):
            self.counter += 1
            return Image(
                id=self.counter,
                name="test",
                original_file_id=1,
                channels=[],
                width=10,
                height=20,
                transcoding_state=ImageTranscodingState.TRANSCODED,
            )

    return TestContext()


class TestTestRunner:
    @mock.patch("cato.runners.test_runner.TestHeartbeatReporter")
    def test_should_report_test_start(
        self, mock_heartbeat_reporter_class, test_context
    ):
        mock_heartbeat_reporter_class.return_value = mock.MagicMock()

        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )
        test_suite = TestSuite(name="suite", tests=[])

        test_context.test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            test_suite,
            test,
        )

        test_context.reporter.report_start_test.assert_called_with(test)
        test_context.command_runner.run.assert_called_with(test.command)
        test_context.output_folder.create_folder("output", test_suite, test)
        time.sleep(1)
        mock_heartbeat_reporter_class.return_value.start_sending_heartbeats_for_test.assert_called_with(
            TestIdentifier("suite", "my_first_test")
        )
        mock_heartbeat_reporter_class.return_value.stop.assert_called_once()
        assert test_context.performance_stats_collector.get_collected_event_names() == {
            "test command execution"
        }

    def test_should_replace_placeholder(self, test_context):
        test = Test(
            name="my_first_test",
            command="crayg -s {{test_resources}}/test.json -o {{image_output_png}}",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )

        test_context.test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        test_context.reporter.report_start_test.assert_called_with(test)
        test_context.command_runner.run.assert_called_with(
            "crayg -s test/suite/my_first_test/test.json -o output/result/suite/my_first_test/my_first_test.png",
        )
        assert test_context.performance_stats_collector.get_collected_event_names() == {
            "test command execution"
        }

    def test_should_collect_timing_info(self, test_context):
        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )

        result = test_context.test_runner.run_test(
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
        assert test_context.performance_stats_collector.get_collected_event_names() == {
            "test command execution"
        }

    def test_should_have_succeded_with_exit_code_0(self, test_context):
        comparison_settings = ComparisonSettings(ComparisonMethod.SSIM, 0.2)
        test_context.output_folder.image_output_exists.return_value = True
        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=comparison_settings,
        )
        test_context.command_runner.run.return_value = CommandResult(
            "dummy_command", 0, []
        )

        result = test_context.test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == ResultStatus.SUCCESS
        assert result.image_output == 2
        assert result.reference_image == 1
        assert result.diff_image == 3
        assert result.failure_reason is None
        test_context.mock_image_comparator.compare.assert_called_with(
            ANY, ANY, comparison_settings, ANY
        )
        assert test_context.performance_stats_collector.get_collected_event_names() == {
            "image comparison",
            "test command execution",
            "upload diff image",
            "upload output image",
            "upload reference image",
        }

    def test_should_have_failed_with_exit_code_0(self, test_context):
        test_context.output_folder.reference_image_exists.return_value = True

        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )
        test_context.command_runner.run.return_value = CommandResult(
            "dummy_command", 1, []
        )

        result = test_context.test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == ResultStatus.FAILED
        assert result.error_value == None
        assert result.failure_reason == TestFailureReason.EXIT_CODE_NON_ZERO
        assert test_context.performance_stats_collector.get_collected_event_names() == {
            "test command execution"
        }

    def test_should_have_failed_with_images_not_equal(self, test_context):
        comparison_settings = ComparisonSettings(ComparisonMethod.SSIM, 0.2)
        test_context.mock_image_comparator.compare.return_value = ComparisonResult(
            status=ResultStatus.FAILED,
            message="Images are not equal!",
            diff_image="diff-image-path.png",
            error=1,
        )
        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=comparison_settings,
        )
        test_context.command_runner.run.return_value = CommandResult(
            "dummy_command", 0, []
        )

        result = test_context.test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == ResultStatus.FAILED
        assert result.message == "Images are not equal!"
        assert result.reference_image == 1
        assert result.image_output == 2
        assert result.diff_image == 3
        assert result.error_value is not None
        assert result.failure_reason == TestFailureReason.IMAGES_ARE_NOT_EQUAL
        assert test_context.mock_cato_api_client.upload_image.call_count == 3
        test_context.mock_image_comparator.compare.assert_called_with(
            ANY, ANY, comparison_settings, ANY
        )
        assert test_context.performance_stats_collector.get_collected_event_names() == {
            "image comparison",
            "test command execution",
            "upload diff image",
            "upload output image",
            "upload reference image",
        }

    def test_should_have_failed_with_missing_reference_image(self, test_context):
        test_context.output_folder.reference_image_exists.return_value = False
        test_context.mock_cato_api_client.compare_images.return_value = (
            CompareImageResult(
                status=ResultStatus.FAILED,
                message="Images are not equal!",
                reference_image_id=1,
                output_image_id=2,
                diff_image_id=3,
                error=1,
            )
        )
        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )
        test_context.command_runner.run.return_value = CommandResult(
            "dummy_command", 0, []
        )

        result = test_context.test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == ResultStatus.FAILED
        assert result.message.startswith("Reference image")
        assert result.image_output == 1
        assert result.reference_image is None
        assert result.diff_image is None
        assert result.error_value == None
        assert result.failure_reason == TestFailureReason.REFERENCE_IMAGE_MISSING
        test_context.reporter.report_message.assert_called_with(result.message)
        assert test_context.mock_cato_api_client.upload_image.call_count == 1
        assert test_context.performance_stats_collector.get_collected_event_names() == {
            "upload output image",
            "test command execution",
        }

    def test_should_have_failed_with_missing_image_output(self, test_context):
        test_context.output_folder.image_output_exists.return_value = False
        test_context.mock_cato_api_client.compare_images.return_value = (
            CompareImageResult(
                status=ResultStatus.FAILED,
                message="Images are not equal!",
                reference_image_id=1,
                output_image_id=2,
                diff_image_id=3,
                error=1,
            )
        )
        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )
        test_context.command_runner.run.return_value = CommandResult(
            "dummy_command", 0, []
        )

        result = test_context.test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == ResultStatus.FAILED
        assert result.message.startswith("No given image output path exists")
        assert result.image_output is None
        assert result.reference_image == 1
        assert result.diff_image is None
        assert result.error_value == None
        assert result.failure_reason == TestFailureReason.OUTPUT_IMAGE_MISSING
        test_context.reporter.report_message.assert_called_with(result.message)
        assert test_context.mock_cato_api_client.upload_image.call_count == 1
        assert test_context.performance_stats_collector.get_collected_event_names() == {
            "upload reference image",
            "test command execution",
        }

    def test_should_have_failed_with_missing_reference_and_image_output(
        self, test_context
    ):
        test_context.output_folder.image_output_exists.return_value = False
        test_context.output_folder.reference_image_exists.return_value = False
        test_context.mock_cato_api_client.compare_images.return_value = (
            CompareImageResult(
                status=ResultStatus.FAILED,
                message="Images are not equal!",
                reference_image_id=1,
                output_image_id=2,
                diff_image_id=3,
                error=1,
            )
        )
        test = Test(
            name="my_first_test",
            command="dummy_command",
            variables={},
            comparison_settings=ComparisonSettings.default(),
        )
        test_context.command_runner.run.return_value = CommandResult(
            "dummy_command", 0, []
        )

        result = test_context.test_runner.run_test(
            RunConfig(
                project_name=EXAMPLE_PROJECT,
                resource_path="test",
                suites=[],
                output_folder="output",
            ),
            TestSuite(name="suite", tests=[]),
            test,
        )

        assert result.status == ResultStatus.FAILED
        assert result.message.startswith("No given image output path exists")
        assert result.image_output is None
        assert result.reference_image is None
        assert result.diff_image is None
        assert result.error_value is None
        assert (
            result.failure_reason
            == TestFailureReason.REFERENCE_AND_OUTPUT_IMAGE_MISSING
        )
        test_context.reporter.report_message.assert_any_call(
            result.message.split(", ")[0]
        )
        test_context.reporter.report_message.assert_any_call(
            result.message.split(", ")[1]
        )
        test_context.mock_cato_api_client.upload_image.assert_not_called()
        assert test_context.performance_stats_collector.get_collected_event_names() == {
            "test command execution"
        }
