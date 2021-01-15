from unittest import mock

import pytest

from cato.reporter.reporter import Reporter
from cato.reporter.verbose_mode import VerboseMode


def test_should_create_with_default_verbode_mode():
    reporter = Reporter()

    assert reporter._verbose_mode == VerboseMode.DEFAULT


def test_should_set_verbode_mode():
    reporter = Reporter()

    reporter.set_verbose_mode(VerboseMode.VERBOSE)

    assert reporter._verbose_mode == VerboseMode.VERBOSE


def test_report_test_command_should_not_report():
    reporter = Reporter()
    reporter.report_message = mock.MagicMock()

    reporter.report_test_command("my command")

    reporter.report_message.assert_not_called()


@pytest.mark.parametrize("mode", [VerboseMode.VERBOSE, VerboseMode.VERY_VERBOSE])
def test_report_test_command_should_report(mode):
    reporter = Reporter()
    reporter.set_verbose_mode(mode)
    reporter.report_message = mock.MagicMock()

    reporter.report_test_command("my command")

    reporter.report_message.assert_called_with("my command")


@pytest.mark.parametrize("mode", [VerboseMode.DEFAULT, VerboseMode.VERBOSE])
def test_report_test_output_should_not_report(mode):
    reporter = Reporter()
    reporter.set_verbose_mode(mode)
    reporter.report_message = mock.MagicMock()

    reporter.report_command_output("my command output")

    reporter.report_message.assert_not_called()


def test_report_test_output_should_report():
    reporter = Reporter()
    reporter.set_verbose_mode(VerboseMode.VERY_VERBOSE)
    reporter.report_message = mock.MagicMock()

    reporter.report_command_output("my command output")

    reporter.report_message.assert_called_with("my command output")
