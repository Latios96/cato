import datetime

from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_result import TestStatus
from cato.domain.test_suite import TestSuite
from cato.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.reporter.stats_calculator import StatsCalculator, Stats


def test_calculates_succeded_correctly():
    test = Test(name="my_first_test", command="dummy_command", variables={})
    test_suite = TestSuite(name="example", tests=[test])
    execution_result = TestExecutionResult(
        test,
        TestStatus.SUCCESS,
        [],
        1,
        "this is a message",
        "",
        datetime.datetime.now(),
        datetime.datetime.now(),
    )
    result = [
        TestSuiteExecutionResult(
            0, 0, test_suite, TestStatus.SUCCESS, [execution_result]
        )
    ]
    stats_calculator = StatsCalculator()

    stats = stats_calculator.calculate(result)

    assert stats == Stats(num_tests=1, succeded_tests=1, failed_tests=0)


def test_calculates_failed_correctly():
    test = Test(name="my_first_test", command="dummy_command", variables={})
    test_suite = TestSuite(name="example", tests=[test])
    execution_result1 = TestExecutionResult(
        test,
        TestStatus.SUCCESS,
        [],
        1,
        "this is a message",
        "",
        datetime.datetime.now(),
        datetime.datetime.now(),
    )
    execution_result2 = TestExecutionResult(
        test,
        TestStatus.FAILED,
        [],
        1,
        "this is a message",
        "",
        datetime.datetime.now(),
        datetime.datetime.now(),
    )
    result = [
        TestSuiteExecutionResult(
            0, 0, test_suite, TestStatus.SUCCESS, [execution_result1, execution_result2]
        )
    ]
    stats_calculator = StatsCalculator()

    stats = stats_calculator.calculate(result)

    assert stats == Stats(num_tests=2, succeded_tests=1, failed_tests=1)
