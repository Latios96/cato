from cato.domain.TestSuite import TestSuite


class Reporter:

    def report_start_test_suite(self, test_suite: TestSuite):
        print(f"Running Test Suite {test_suite.name}...")
