import datetime

import emoji

from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_status import TestStatus
from cato.domain.test_suite import TestSuite
from cato.file_system_abstractions.output_folder import OutputFolder
from cato.image_utils.image_comparator import ImageComparator
from cato.reporter.reporter import Reporter
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.reporter.test_heartbeat_reporter import TestHeartbeatReporter
from cato.runners.command_runner import CommandRunner
from cato.variable_processing.variable_predefinition import PREDEFINITIONS
from cato.variable_processing.variable_processor import VariableProcessor
from cato_server.domain.test_identifier import TestIdentifier


class TestRunner:
    __test__ = False

    def __init__(
        self,
        command_runner: CommandRunner,
        reporter: Reporter,
        output_folder: OutputFolder,
        image_comparator: ImageComparator,
        test_execution_reporter: TestExecutionReporter,
    ):
        self._command_runner = command_runner
        self._reporter = reporter
        self._output_folder = output_folder
        self._variable_processor = VariableProcessor()
        self._image_comparator = image_comparator
        self._test_execution_reporter = test_execution_reporter

    def run_test(self, config: Config, current_suite: TestSuite, test: Test):
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

    def _run_test(self, config: Config, current_suite: TestSuite, test: Test):
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
                start,
                end,
            )

        image_output = self._output_folder.any_existing(self._image_outputs(variables))
        if not image_output or not self._output_folder.image_output_exists(
            image_output
        ):
            image_output_str = emoji.emojize(
                ":x:\n".join(self._image_outputs(variables)), use_aliases=True
            )
            message = emoji.emojize(
                f"No given image output path exists: \n{image_output_str} :x:",
                use_aliases=True,
            )
            self._reporter.report_message(message)
            return TestExecutionResult(
                test,
                TestStatus.FAILED,
                command_result.output,
                elapsed,
                message,
                None,
                None,
                start,
                end,
            )

        reference_image = self._output_folder.any_existing(
            self._reference_images(variables)
        )
        if not reference_image or not self._output_folder.reference_image_exists(
            reference_image
        ):
            return TestExecutionResult(
                test,
                TestStatus.FAILED,
                command_result.output,
                elapsed,
                f"Reference image {reference_image if reference_image else '<not found>'} does not exist!",
                image_output,
                None,
                start,
                end,
            )

        image_compare_result = self._image_comparator.compare(
            reference_image, image_output
        )
        if image_compare_result.error:
            return TestExecutionResult(
                test,
                TestStatus.FAILED,
                command_result.output,
                elapsed,
                "Images are not equal!",
                image_output,
                reference_image,
                start,
                end,
            )

        return TestExecutionResult(
            test,
            TestStatus.SUCCESS,
            command_result.output,
            elapsed,
            message="",
            image_output=image_output,
            reference_image=reference_image,
            started_at=start,
            finished_at=end,
        )

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
