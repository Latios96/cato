from unittest import mock

import pytest

from cato.domain.Test import Test
from cato.domain.TestSuite import TestSuite
from cato.reporter.Reporter import Reporter
from cato.runners.TestSuiteRunner import TestSuiteRunner
from tests.utils import mock_safe
from cato.runners.TestRunner import TestRunner


def test_run_empty_suites_should_fail():
    mock_reporter = mock_safe(Reporter)
    mock_test_runner = mock_safe(TestRunner)
    test_suite_runner = TestSuiteRunner(mock_test_runner, mock_reporter)

    with pytest.raises(ValueError):
        test_suite_runner.run_test_suites([])


def test_run_suite_should_report_start_and_delegate_to_test_runner():
    mock_reporter = mock_safe(Reporter)
    mock_test_runner = mock_safe(TestRunner)
    test_suite_runner = TestSuiteRunner(mock_test_runner, mock_reporter)
    test = Test(name="my first test", command="dummy_command")
    test_suite = TestSuite(name="example", tests=[test])

    test_suite_runner.run_test_suites([test_suite])

    mock_reporter.report_start_test_suite.assert_called_once()
    mock_test_runner.run_test.assert_called_with(test)
