import pinject

from cato.domain.Test import Test
from cato.domain.TestSuite import TestSuite
from cato.runners.TestSuiteRunner import TestSuiteRunner

if __name__ == "__main__":
    test_suite = TestSuite(name="example", tests=[Test(name="my first test")])

    obj_graph = pinject.new_object_graph()
    test_suite_runner = obj_graph.provide(TestSuiteRunner)

    test_suite_runner.run_test_suites([test_suite])
