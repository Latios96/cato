import os

from contexttimer import Timer

from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_result import TestResult
from cato.domain.test_suite import TestSuite
from cato.reporter.reporter import Reporter
from cato.runners.command_runner import CommandRunner


class TestRunner:
    def __init__(self, command_runner: CommandRunner, reporter: Reporter):
        self._command_runner = command_runner
        self._reporter = reporter

    def run_test(self, config: Config, current_suite: TestSuite, test: Test):
        self._reporter.report_start_test(test)

        command = self._prepare_command(config, current_suite, test)

        with Timer() as t:
            command_result = self._command_runner.run(command)
            print(t.elapsed)
            return TestExecutionResult(test, TestResult.SUCCESS, command_result.output, t.elapsed)

    def _prepare_command(self, config, current_suite, test):
        command_variables = {
            "test_resources": os.path.join(config.path, current_suite.name, test.name),
            "image_output_png": os.path.join("result", "{}.png".format(test.name)),
        }
        command = test.command.format(**command_variables)
        return command
