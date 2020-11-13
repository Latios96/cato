import emoji

from cato.domain.test import Test
from cato.domain.test_suite import TestSuite


class Reporter:
    def report_start_test_suite(self, test_suite: TestSuite):
        print(f"Running Test Suite {test_suite.name}..")

    def report_start_test(self, test: Test):
        print(f"{test.name}..")

    def report_test_sucess(self, test):
        print(
            emoji.emojize(
                f"\n{test.name} succeded :white_check_mark:", use_aliases=True
            )
        )

    def report_test_failure(self, test):
        print(emoji.emojize(f"\n{test.name} failed :x:", use_aliases=True))
