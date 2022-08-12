from cato.domain.comparison_settings import ComparisonSettings
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato_common.domain.result_status import ResultStatus
from cato.domain.test_suite import TestSuite
from cato.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.reporter.timing_report_generator import TimingReportGenerator
from cato_common.utils.datetime_utils import aware_now_in_utc


def test_generate():
    generator = TimingReportGenerator()

    test = Test("my_test", "cmd", {}, comparison_settings=ComparisonSettings.default())
    test2 = Test("my_test", "cmd", {}, comparison_settings=ComparisonSettings.default())
    report = generator.generate(
        [
            TestSuiteExecutionResult(
                TestSuite(name="test_suite", tests=[test, test2]),
                test_results=[
                    TestExecutionResult(
                        test,
                        ResultStatus.SUCCESS,
                        [],
                        50,
                        "this is a message",
                        None,
                        None,
                        None,
                        aware_now_in_utc(),
                        aware_now_in_utc(),
                        1,
                        failure_reason=None,
                    ),
                    TestExecutionResult(
                        test2,
                        ResultStatus.SUCCESS,
                        [],
                        500,
                        "this is a message",
                        None,
                        None,
                        None,
                        aware_now_in_utc(),
                        aware_now_in_utc(),
                        1,
                        failure_reason=None,
                    ),
                ],
                result=ResultStatus.SUCCESS,
            )
        ]
    )
    assert (
        report
        == """
Test                Duration                  Result
------------------  ------------------------  --------
test_suite/my_test  50 seconds                ✅
test_suite/my_test  8 minutes and 20 seconds  ✅"""[
            1:
        ]
    )
