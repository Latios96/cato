import tempfile

import emoji

from cato.reporter.performance_stats_collector import (
    ImageType,
    PerformanceStatsCollector,
)
from cato_common.domain.config import RunConfig
from cato_common.domain.test import Test
from cato_common.domain.test_execution_result import TestExecutionResult
from cato_common.domain.test_suite import TestSuite
from cato.file_system_abstractions.output_folder import OutputFolder
from cato.reporter.reporter import Reporter
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.reporter.test_heartbeat_reporter import TestHeartbeatReporter
from cato.runners.command_runner import CommandRunner
from cato.variable_processing.variable_predefinition import PREDEFINITIONS
from cato.variable_processing.variable_processor import VariableProcessor
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.utils.datetime_utils import aware_now_in_utc
from cato_common.images.image_comparators.image_comparator import ImageComparator


class TestRunner:
    __test__ = False

    def __init__(
        self,
        command_runner: CommandRunner,
        reporter: Reporter,
        output_folder: OutputFolder,
        test_execution_reporter: TestExecutionReporter,
        cato_api_client: CatoApiClient,
        image_comparator: ImageComparator,
        performance_stats_collector: PerformanceStatsCollector,
    ):
        self._command_runner = command_runner
        self._reporter = reporter
        self._output_folder = output_folder
        self._variable_processor = VariableProcessor()
        self._test_execution_reporter = test_execution_reporter
        self._cato_api_client = cato_api_client
        self._image_comparator = image_comparator
        self._performance_stats_collector = performance_stats_collector

    def run_test(
        self, config: RunConfig, current_suite: TestSuite, test: Test
    ) -> TestExecutionResult:
        self._reporter.report_start_test(test)
        test_heartbeat_reporter = TestHeartbeatReporter(self._test_execution_reporter)

        test_heartbeat_reporter.start_sending_heartbeats_for_test(
            TestIdentifier(current_suite.name, test.name)
        )
        try:
            result = self._run_test(config, current_suite, test)
        except (Exception, KeyboardInterrupt) as e:
            test_heartbeat_reporter.stop()
            raise e
        test_heartbeat_reporter.stop()

        return result

    def _run_test(
        self, config: RunConfig, current_suite: TestSuite, test: Test
    ) -> TestExecutionResult:
        variables = self._variable_processor.evaluate_variables(
            config, current_suite, test, predefinitions=PREDEFINITIONS
        )

        command = self._variable_processor.format_command(test.command, variables)

        self._output_folder.create_folder(config.output_folder, current_suite, test)

        start = aware_now_in_utc()

        self._reporter.report_test_command('Command: "{}"'.format(command))
        with self._performance_stats_collector.collect_test_command_execution_timing():
            command_result = self._command_runner.run(command)

        end = aware_now_in_utc()
        elapsed = (end - start).total_seconds()

        if command_result.exit_code != 0:
            # todo if exit code is not none, also compare images, but fail test in any case
            return TestExecutionResult(
                test,
                ResultStatus.FAILED,
                command_result.output,
                elapsed,
                f"Command exited with exit code {command_result.exit_code}",
                None,
                None,
                None,
                start,
                end,
                error_value=None,
                failure_reason=TestFailureReason.EXIT_CODE_NON_ZERO,
            )

        image_output = self._output_folder.any_existing(self._image_outputs(variables))
        no_image_output = (
            image_output is None
            or not self._output_folder.image_output_exists(image_output)
        )
        image_output_str = emoji.emojize(
            ":x:\n".join(self._image_outputs(variables)), language="alias"
        )
        message_image_output_missing = emoji.emojize(
            f"No given image output path exists: \n{image_output_str} :x:",
            language="alias",
        )

        reference_image = self._output_folder.any_existing(
            self._reference_images(variables)
        )
        no_reference_image = (
            reference_image is None
            or not self._output_folder.reference_image_exists(reference_image)
        )
        message_reference_image_missing = f"Reference image {reference_image if reference_image else '<not found>'} does not exist!"

        if no_reference_image and not no_image_output and image_output is not None:
            self._reporter.report_message(message_reference_image_missing)
            with self._performance_stats_collector.collect_image_upload_timing(
                ImageType.OUTPUT
            ):
                image_output_image = self._cato_api_client.upload_image(image_output)
            return TestExecutionResult(
                test,
                ResultStatus.FAILED,
                command_result.output,
                elapsed,
                message_reference_image_missing,
                image_output_image.id,
                None,
                None,
                start,
                end,
                error_value=None,
                failure_reason=TestFailureReason.REFERENCE_IMAGE_MISSING,
            )

        if no_image_output and not no_reference_image and reference_image is not None:
            self._reporter.report_message(message_image_output_missing)
            with self._performance_stats_collector.collect_image_upload_timing(
                ImageType.REFERENCE
            ):
                reference_image_image = self._cato_api_client.upload_image(
                    reference_image
                )
            return TestExecutionResult(
                test,
                ResultStatus.FAILED,
                command_result.output,
                elapsed,
                message_image_output_missing,
                None,
                reference_image_image.id,
                None,
                start,
                end,
                error_value=None,
                failure_reason=TestFailureReason.OUTPUT_IMAGE_MISSING,
            )

        if no_image_output and no_reference_image:
            self._reporter.report_message(message_image_output_missing)
            self._reporter.report_message(message_reference_image_missing)
            return TestExecutionResult(
                test,
                ResultStatus.FAILED,
                command_result.output,
                elapsed,
                "{}, {}".format(
                    message_image_output_missing, message_reference_image_missing
                ),
                None,
                None,
                None,
                start,
                end,
                error_value=None,
                failure_reason=TestFailureReason.REFERENCE_AND_OUTPUT_IMAGE_MISSING,
            )
        self._reporter.report_message(
            "Found image output at path {}".format(image_output)
        )
        self._reporter.report_message(
            "Found reference image at path {}".format(reference_image)
        )
        if reference_image is not None and image_output is not None:
            self._reporter.report_message("Comparing images locally..")

            with tempfile.TemporaryDirectory() as tmpdirname:
                with self._performance_stats_collector.collect_image_comparison_timing():
                    image_compare_result = self._image_comparator.compare(
                        reference_image,
                        image_output,
                        test.comparison_settings,
                        tmpdirname,
                    )

                with self._performance_stats_collector.collect_image_upload_timing(
                    ImageType.REFERENCE
                ):
                    reference_image_id = self._cato_api_client.upload_image(
                        reference_image
                    ).id
                with self._performance_stats_collector.collect_image_upload_timing(
                    ImageType.OUTPUT
                ):
                    output_image_id = self._cato_api_client.upload_image(
                        image_output
                    ).id
                diff_image_id = None
                if image_compare_result.diff_image:
                    with self._performance_stats_collector.collect_image_upload_timing(
                        ImageType.DIFF
                    ):
                        diff_image_id = self._cato_api_client.upload_image(
                            image_compare_result.diff_image
                        ).id

            if image_compare_result.status == ResultStatus.FAILED:
                return TestExecutionResult(
                    test,
                    ResultStatus.FAILED,
                    command_result.output,
                    elapsed,
                    (
                        image_compare_result.message
                        if image_compare_result.message
                        else ""
                    ),
                    output_image_id,
                    reference_image_id,
                    diff_image_id,
                    start,
                    end,
                    error_value=image_compare_result.error,
                    failure_reason=TestFailureReason.IMAGES_ARE_NOT_EQUAL,
                )

            return TestExecutionResult(
                test,
                ResultStatus.SUCCESS,
                command_result.output,
                elapsed,
                message="",
                image_output=output_image_id,
                reference_image=reference_image_id,
                diff_image=diff_image_id,
                started_at=start,
                finished_at=end,
                error_value=image_compare_result.error,
                failure_reason=None,
            )
        raise RuntimeError("This should never happen!")

    def _image_outputs(self, variables):
        image_outputs = [
            variables.get("image_output"),
            variables.get("image_output_png"),
            variables.get("image_output_exr"),
            variables.get("image_output_jpg"),
            variables.get("image_output_tif"),
        ]
        return list(filter(lambda x: x is not None, image_outputs))

    def _reference_images(self, variables):
        image_outputs = [
            variables.get("reference_image"),
            variables.get("reference_image_png"),
            variables.get("reference_image_exr"),
            variables.get("reference_image_jpg"),
            variables.get("reference_image_tif"),
        ]
        return list(filter(lambda x: x is not None, image_outputs))
