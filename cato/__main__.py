from cato.domain.Test import Test
from cato.domain.TestSuite import TestSuite
from cato.reporter.Reporter import Reporter
from cato.runners.TestSuiteRunner import TestSuiteRunner

if __name__ == "__main__":
    test_suite = TestSuite(name="example", tests=[Test(name="my first test")])

    runner = TestSuiteRunner(TestRunner(), Reporter())
    runner.run_test_suites([test_suite])
