import os
import pprint

import emoji
from contexttimer import Timer

from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_result import TestStatus
from cato.domain.test_suite import TestSuite
from cato.image_comparison.image_comparator import ImageComparator
from cato.reporter.reporter import Reporter
from cato.runners.command_runner import CommandRunner
from cato.runners.output_folder import OutputFolder
from cato.runners.variable_processor import VariableProcessor


class TestRunner:
    def __init__(
        self,
        command_runner: CommandRunner,
        reporter: Reporter,
        output_folder: OutputFolder,
        image_comparator: ImageComparator,
    ):
        self._command_runner = command_runner
        self._reporter = reporter
        self._output_folder = output_folder
        self._variable_processor = VariableProcessor()
        self._image_comparator = image_comparator

    def run_test(self, config: Config, current_suite: TestSuite, test: Test):
        self._reporter.report_start_test(test)

        variables = self._variable_processor.evaluate_variables(
            config, current_suite, test, test.variables
        )

        command = self._variable_processor.format_command(test.command, variables)

        self._output_folder.create_folder(config.output_folder, current_suite, test)

        with Timer() as t:
            self._reporter.report_message('Command: "{}"'.format(command))
            command_result = self._command_runner.run(command)

        if command_result.exit_code != 0:
            return TestExecutionResult(
                test,
                TestStatus.FAILED,
                command_result.output,
                t.elapsed,
                f"Command exited with exit code {command_result.exit_code}",
                "",
            )

        image_output = self._output_folder.any_existing(self._image_outputs(variables))
        if not image_output:
            image_output_str = emoji.emojize(
                ":x:\n".join(self._image_outputs(variables)), use_aliases=True
            )
            message = emoji.emojize(
                f"No given image output path exists: \n{image_output_str} :x:",
                use_aliases=True,
            )
            self._reporter.report_message(message)
            return TestExecutionResult(
                test, TestStatus.FAILED, command_result.output, t.elapsed, message, ""
            )

        reference_image = self._output_folder.any_existing(
            self._reference_images(variables)
        )
        if not self._output_folder.reference_image_exists(reference_image):
            return TestExecutionResult(
                test,
                TestStatus.FAILED,
                command_result.output,
                t.elapsed,
                f"Reference image {reference_image} does not exist!",
                image_output,
            )

        image_compare_result = self._image_comparator.compare(
            reference_image, image_output
        )
        if image_compare_result.error:
            return TestExecutionResult(
                test,
                TestStatus.FAILED,
                command_result.output,
                t.elapsed,
                "Images are not equal!",
                image_output,
            )

        return TestExecutionResult(
            test,
            TestStatus.SUCCESS,
            command_result.output,
            t.elapsed,
            message="",
            image_output=image_output,
        )

    def _image_output_exists(self, variables):
        image_outputs = self._image_outputs(variables)
        for output in image_outputs:
            if self._output_folder.image_output_exists(output):
                return output
        return None

    def _image_outputs(self, variables):
        image_outputs = [
            variables.get("image_output"),
            variables.get("image_output_png"),
            variables.get("image_output_exr"),
        ]
        return list(filter(lambda x: x != None, image_outputs))

    def _reference_images(self, variables):
        image_outputs = [
            variables.get("reference_image"),
            variables.get("reference_image_png"),
            variables.get("reference_image_exr"),
        ]
        return list(filter(lambda x: x != None, image_outputs))
