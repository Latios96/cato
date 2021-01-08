import logging
import emoji
import humanfriendly

from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_suite import TestSuite
from cato.reporter.verbose_mode import VerboseMode

logger = logging.getLogger(__name__)


class Reporter:
    def __init__(self):
        self._verbose_mode = VerboseMode.DEFAULT

    def set_verbose_mode(self, verbose_mode: VerboseMode):
        self._verbose_mode = verbose_mode

    def report_message(self, message):
        logger.info(message)

    def report_start_test_suite(self, test_suite: TestSuite):
        self.report_message(f"Running Test Suite {test_suite.name}..")

    def report_start_test(self, test: Test):
        self.report_message(f"Running {test.name}..")

    def report_test_success(self, result: TestExecutionResult):
        self.report_message(
            emoji.emojize(
                f"{result.test.name} succeeded in {humanfriendly.format_timespan(result.seconds)} :white_check_mark:",
                use_aliases=True,
            )
        )

    def report_test_failure(self, test_result: TestExecutionResult):
        self.report_message(
            emoji.emojize(
                f"\n{test_result.test.name} failed :x:: {test_result.message}",
                use_aliases=True,
            )
        )

    def report_test_command(self, command: str):
        if self._verbose_mode.includes(VerboseMode.VERBOSE):
            self.report_message(command)

    def report_command_output(self, output_line: str):
        if self._verbose_mode.includes(VerboseMode.VERY_VERBOSE):
            self.report_message(output_line)
