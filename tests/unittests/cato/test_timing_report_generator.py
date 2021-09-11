import datetime

from cato.domain.comparison_settings import ComparisonSettings
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_status import TestStatus
from cato.domain.test_suite import TestSuite
from cato.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.reporter.timing_report_generator import TimingReportGenerator


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
                        TestStatus.SUCCESS,
                        [],
                        50,
                        "this is a message",
                        None,
                        None,
                        None,
                        datetime.datetime.now(),
                        datetime.datetime.now(),
                        1,
                    ),
                    TestExecutionResult(
                        test2,
                        TestStatus.SUCCESS,
                        [],
                        500,
                        "this is a message",
                        None,
                        None,
                        None,
                        datetime.datetime.now(),
                        datetime.datetime.now(),
                        1,
                    ),
                ],
                result=TestStatus.SUCCESS,
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
