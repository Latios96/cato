from cato.domain.test import Test
from cato.reporter.reporter import Reporter
from cato.runners.command_runner import CommandRunner
from cato.runners.test_runner import TestRunner
from tests.utils import mock_safe


def test_should_report_test_start():
    reporter = mock_safe(Reporter)
    command_runner = mock_safe(CommandRunner)
    test_runner = TestRunner(command_runner, reporter)
    test = Test(name="my first test", command="dummy_command")

    test_runner.run_test(test)

    reporter.report_start_test.assert_called_with(test)
    command_runner.run.assert_called_with(test.command)
