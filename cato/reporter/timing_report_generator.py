from typing import List, Tuple, Iterable

import emoji
import humanfriendly
from tabulate import tabulate

from cato_common.domain.test_execution_result import TestExecutionResult
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.test_suite_execution_result import TestSuiteExecutionResult


def iterate_suite_results(
    results: List[TestSuiteExecutionResult],
) -> Iterable[Tuple[TestSuiteExecutionResult, TestExecutionResult]]:
    for suite_result in results:
        for test_result in suite_result.test_results:
            yield suite_result, test_result


class TimingReportGenerator:
    def generate(self, suite_results: List[TestSuiteExecutionResult]) -> str:
        entries = []

        for suite_result, test_result in iterate_suite_results(suite_results):
            name = f"{suite_result.test_suite.name}/{test_result.test.name}"
            duration = humanfriendly.format_timespan(test_result.seconds)
            result = (
                emoji.emojize(":white_check_mark:", language="alias")
                if test_result.status == ResultStatus.SUCCESS
                else emoji.emojize(":x:", language="alias")
            )
            entries.append((name, duration, result))

        return tabulate(entries, headers=["Test", "Duration", "Result"])
