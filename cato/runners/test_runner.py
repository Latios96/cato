import os

from contexttimer import Timer

from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_result import TestStatus
from cato.domain.test_suite import TestSuite
from cato.reporter.reporter import Reporter
from cato.runners.command_runner import CommandRunner
from cato.runners.output_folder_creator import OutputFolderCreator


class TestRunner:
    def __init__(
        self,
        command_runner: CommandRunner,
        reporter: Reporter,
        output_folder_creator: OutputFolderCreator,
    ):
        self._command_runner = command_runner
        self._reporter = reporter
        self._output_folder_creator = output_folder_creator

    def run_test(self, config: Config, current_suite: TestSuite, test: Test):
        self._reporter.report_start_test(test)

        command = self._prepare_command(config, current_suite, test)

        self._output_folder_creator.create_folder(
            config.output_folder, current_suite, test
        )

        with Timer() as t:
            self._reporter.report_message('Command: "{}"'.format(command))
            command_result = self._command_runner.run(command)

        if command_result.exit_code == 0:
            return TestExecutionResult(
                test, TestStatus.SUCCESS, command_result.output, t.elapsed
            )

        return TestExecutionResult(
            test, TestStatus.FAILED, command_result.output, t.elapsed
        )

    def _prepare_command(self, config, current_suite, test):
        command_variables = {
            "test_resources": os.path.join(config.path, current_suite.name, test.name),
            "image_output_png": os.path.join(
                config.output_folder,
                "result",
                current_suite.name,
                test.name,
                "{}.png".format(test.name),
            ),
            "image_output_no_extension": os.path.join(
                config.output_folder, "result", current_suite.name, test.name, test.name
            ),
        }
        command = test.command.format(**command_variables)
        return command
