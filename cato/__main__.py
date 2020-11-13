import pinject

from cato.domain.test import Test
from cato.domain.test_suite import TestSuite
from cato.runners.test_suite_runner import TestSuiteRunner

if __name__ == "__main__":
    test_suite = TestSuite(
        name="example", tests=[Test(name="my first test", command=["python", "--version"])]
    )

    obj_graph = pinject.new_object_graph()
    test_suite_runner = obj_graph.provide(TestSuiteRunner)

    test_suite_runner.run_test_suites([test_suite])
