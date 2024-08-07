from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.test import Test
from cato_common.domain.test_execution_result import TestExecutionResult
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.test_suite import TestSuite
from cato_common.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.reporter.stats_calculator import StatsCalculator, Stats
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.utils.datetime_utils import aware_now_in_utc

MESSAGE = "this is a message"


def test_calculates_succeded_correctly():
    test = Test(
        name="my_first_test",
        command="dummy_command",
        variables={},
        comparison_settings=ComparisonSettings.default(),
    )
    test_suite = TestSuite(name="example", tests=[test])
    execution_result = TestExecutionResult(
        test,
        ResultStatus.SUCCESS,
        [],
        1,
        MESSAGE,
        None,
        None,
        None,
        aware_now_in_utc(),
        aware_now_in_utc(),
        1,
        failure_reason=None,
    )
    result = [
        TestSuiteExecutionResult(test_suite, ResultStatus.SUCCESS, [execution_result])
    ]
    stats_calculator = StatsCalculator()

    stats = stats_calculator.calculate(result)

    assert stats == Stats(num_tests=1, succeded_tests=1, failed_tests=0)


def test_calculates_failed_correctly():
    test = Test(
        name="my_first_test",
        command="dummy_command",
        variables={},
        comparison_settings=ComparisonSettings.default(),
    )
    test_suite = TestSuite(name="example", tests=[test])
    execution_result1 = TestExecutionResult(
        test,
        ResultStatus.SUCCESS,
        [],
        1,
        MESSAGE,
        None,
        None,
        None,
        aware_now_in_utc(),
        aware_now_in_utc(),
        1,
        failure_reason=None,
    )
    execution_result2 = TestExecutionResult(
        test,
        ResultStatus.FAILED,
        [],
        1,
        MESSAGE,
        None,
        None,
        None,
        aware_now_in_utc(),
        aware_now_in_utc(),
        1,
        failure_reason=TestFailureReason.REFERENCE_IMAGE_MISSING,
    )
    result = [
        TestSuiteExecutionResult(
            test_suite, ResultStatus.SUCCESS, [execution_result1, execution_result2]
        )
    ]
    stats_calculator = StatsCalculator()

    stats = stats_calculator.calculate(result)

    assert stats == Stats(num_tests=2, succeded_tests=1, failed_tests=1)
