from cato.domain.test import Test
from cato.reporter.reporter import Reporter
from cato.runners.command_runner import CommandRunner


class TestRunner:
    def __init__(self, command_runner: CommandRunner, reporter: Reporter):
        self._command_runner = command_runner
        self._reporter = reporter

    def run_test(self, test: Test):
        self._reporter.report_start_test(test)

        self._command_runner.run(test.command)
