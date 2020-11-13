from cato.domain.Test import Test
from cato.reporter.Reporter import Reporter
from cato.runners.TestRunner import TestRunner
from tests.utils import mock_safe


def should_report_test_start():
    reporter = mock_safe(Reporter)
    test_runner = TestRunner(reporter)
    test = Test(name="my first test", command="dummy_command")

    test_runner.run_test(test)

    reporter.report_start_test.assert_called_with(test)
