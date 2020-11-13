from cato.domain.test import Test
from cato.domain.test_suite import TestSuite


class Reporter:
    def report_start_test_suite(self, test_suite: TestSuite):
        print(f"Running Test Suite {test_suite.name}..")

    def report_start_test(self, test: Test):
        print(f"{test.name}..")
