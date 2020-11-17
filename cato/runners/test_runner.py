import os
import pprint

import emoji
from contexttimer import Timer

from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_result import TestStatus
from cato.domain.test_suite import TestSuite
from cato.reporter.reporter import Reporter
from cato.runners.command_runner import CommandRunner
from cato.runners.output_folder_creator import OutputFolder
from cato.runners.variable_processor import VariableProcessor


class TestRunner:
    def __init__(
        self,
        command_runner: CommandRunner,
        reporter: Reporter,
        output_folder: OutputFolder,
    ):
        self._command_runner = command_runner
        self._reporter = reporter
        self._output_folder = output_folder
        self._variable_processor = VariableProcessor()

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
                test, TestStatus.FAILED, command_result.output, t.elapsed, f"Command exited with exit code {command_result.exit_code}"
            )

        if not self._image_output_exists(variables):
            image_output_str = emoji.emojize(
                ":x:\n".join(self._image_outputs(variables)), use_aliases=True
            )
            message = emoji.emojize(f"No given image output path exists: \n{image_output_str} :x:", use_aliases=True, )
            self._reporter.report_message(
                message
            )
            return TestExecutionResult(
                test, TestStatus.FAILED, command_result.output, t.elapsed, message
            )

        return TestExecutionResult(
            test, TestStatus.SUCCESS, command_result.output, t.elapsed, message=""
        )

    def _image_output_exists(self, variables):
        image_outputs = self._image_outputs(variables)
        for output in image_outputs:
            if self._output_folder.image_output_exists(output):
                return True
        return False

    def _image_outputs(self, variables):
        image_outputs = [
            variables.get("image_output"),
            variables.get("image_output_png"),
            variables.get("image_output_exr"),
        ]
        return list(filter(lambda x: x != None, image_outputs))
