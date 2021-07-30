import datetime

import emoji

from cato.domain.config import RunConfig
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_status import TestStatus
from cato.domain.test_suite import TestSuite
from cato.file_system_abstractions.output_folder import OutputFolder
from cato.reporter.reporter import Reporter
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.reporter.test_heartbeat_reporter import TestHeartbeatReporter
from cato.runners.command_runner import CommandRunner
from cato.variable_processing.variable_predefinition import PREDEFINITIONS
from cato.variable_processing.variable_processor import VariableProcessor
from cato_api_client.cato_api_client import CatoApiClient
from cato_server.domain.test_identifier import TestIdentifier


class TestRunner:
    __test__ = False

    def __init__(
        self,
        command_runner: CommandRunner,
        reporter: Reporter,
        output_folder: OutputFolder,
        test_execution_reporter: TestExecutionReporter,
        cato_api_client: CatoApiClient,
    ):
        self._command_runner = command_runner
        self._reporter = reporter
        self._output_folder = output_folder
        self._variable_processor = VariableProcessor()
        self._test_execution_reporter = test_execution_reporter
        self._cato_api_client = cato_api_client

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

        start = datetime.datetime.now()

        self._reporter.report_test_command('Command: "{}"'.format(command))
        command_result = self._command_runner.run(command)

        end = datetime.datetime.now()
        elapsed = (end - start).total_seconds()

        if command_result.exit_code != 0:
            return TestExecutionResult(
                test,
                TestStatus.FAILED,
                command_result.output,
                elapsed,
                f"Command exited with exit code {command_result.exit_code}",
                None,
                None,
                None,
                start,
                end,
            )

        image_output = self._output_folder.any_existing(self._image_outputs(variables))
        no_image_output = (
            image_output is None
            or not self._output_folder.image_output_exists(image_output)
        )
        image_output_str = emoji.emojize(
            ":x:\n".join(self._image_outputs(variables)), use_aliases=True
        )
        message_image_output_missing = emoji.emojize(
            f"No given image output path exists: \n{image_output_str} :x:",
            use_aliases=True,
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
            image_output_image = self._cato_api_client.upload_image(image_output)
            return TestExecutionResult(
                test,
                TestStatus.FAILED,
                command_result.output,
                elapsed,
                message_reference_image_missing,
                image_output_image.id,
                None,
                None,
                start,
                end,
            )

        if no_image_output and not no_reference_image and reference_image is not None:
            self._reporter.report_message(message_image_output_missing)
            reference_image_image = self._cato_api_client.upload_image(reference_image)
            return TestExecutionResult(
                test,
                TestStatus.FAILED,
                command_result.output,
                elapsed,
                message_image_output_missing,
                None,
                reference_image_image.id,
                None,
                start,
                end,
            )

        if no_image_output and no_reference_image:
            self._reporter.report_message(message_image_output_missing)
            self._reporter.report_message(message_reference_image_missing)
            return TestExecutionResult(
                test,
                TestStatus.FAILED,
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
            )
        self._reporter.report_message(
            "Found image output at path {}".format(image_output)
        )
        self._reporter.report_message(
            "Found reference image at path {}".format(reference_image)
        )
        if reference_image is not None and image_output is not None:
            image_compare_result = self._cato_api_client.compare_images(
                reference_image,
                image_output,
                test.comparison_settings,
            )

            if image_compare_result.status == TestStatus.FAILED:
                return TestExecutionResult(
                    test,
                    TestStatus.FAILED,
                    command_result.output,
                    elapsed,
                    image_compare_result.message
                    if image_compare_result.message
                    else "",
                    image_compare_result.reference_image_id,
                    image_compare_result.output_image_id,
                    image_compare_result.diff_image_id,
                    start,
                    end,
                )

            return TestExecutionResult(
                test,
                TestStatus.SUCCESS,
                command_result.output,
                elapsed,
                message="",
                image_output=image_compare_result.output_image_id,
                reference_image=image_compare_result.reference_image_id,
                diff_image=image_compare_result.diff_image_id,
                started_at=start,
                finished_at=end,
            )
        raise RuntimeError("This should never happen!")

    def _image_outputs(self, variables):
        image_outputs = [
            variables.get("image_output"),
            variables.get("image_output_png"),
            variables.get("image_output_exr"),
        ]
        return list(filter(lambda x: x is not None, image_outputs))

    def _reference_images(self, variables):
        image_outputs = [
            variables.get("reference_image"),
            variables.get("reference_image_png"),
            variables.get("reference_image_exr"),
        ]
        return list(filter(lambda x: x is not None, image_outputs))
