import logging
import emoji
import humanfriendly

from cato_common.domain.test import Test
from cato_common.domain.test_execution_result import TestExecutionResult
from cato_common.domain.test_suite import TestSuite
from cato.reporter.verbose_mode import VerboseMode

logger = logging.getLogger(__name__)


class Reporter:
    def __init__(self) -> None:
        self._verbose_mode = VerboseMode.DEFAULT

    def set_verbose_mode(self, verbose_mode: VerboseMode) -> None:
        self._verbose_mode = verbose_mode

    def report_message(self, message: str) -> None:
        logger.info(message)

    def report_start_test_suite(self, test_suite: TestSuite) -> None:
        self.report_message(f"Running Test Suite {test_suite.name}..")

    def report_start_test(self, test: Test) -> None:
        self.report_message(f"Running {test.name}..")

    def report_test_success(self, result: TestExecutionResult) -> None:
        self.report_message(
            emoji.emojize(
                f"{result.test.name} succeeded in {humanfriendly.format_timespan(result.seconds)} :white_check_mark:",
                language="alias",
            )
        )

    def report_test_failure(self, test_result: TestExecutionResult) -> None:
        self.report_message(
            emoji.emojize(
                f"\n{test_result.test.name} failed :x:: {test_result.message}",
                language="alias",
            )
        )

    def report_test_command(self, command: str) -> None:
        if self._verbose_mode.includes(VerboseMode.VERBOSE):
            self.report_message(command)

    def report_command_output(self, output_line: str) -> None:
        if self._verbose_mode.includes(VerboseMode.VERY_VERBOSE):
            self.report_message(output_line)
