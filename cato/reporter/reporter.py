import emoji
import humanfriendly

from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_suite import TestSuite


class Reporter:
    def report_message(self, message):
        print(message)

    def report_start_test_suite(self, test_suite: TestSuite):
        self.report_message(f"Running Test Suite {test_suite.name}..")

    def report_start_test(self, test: Test):
        self.report_message(f"Running {test.name}..")

    def report_test_sucess(self, result: TestExecutionResult):
        self.report_message(
            emoji.emojize(
                f"\n{result.test.name} succeeded in {humanfriendly.format_timespan(result.seconds)} :white_check_mark:",
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
