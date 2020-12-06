import itertools
from dataclasses import dataclass
from typing import List

from cato.domain.test_status import TestStatus
from cato.domain.test_suite_execution_result import TestSuiteExecutionResult


@dataclass
class Stats:
    num_tests: int
    succeded_tests: int
    failed_tests: int


class StatsCalculator:
    def calculate(self, result: List[TestSuiteExecutionResult]) -> Stats:
        all_tests = list(itertools.chain(*map(lambda x: x.test_results, result)))

        total_tests = len(all_tests)

        total_tests_succeded = len(
            list(filter(lambda x: x.status == TestStatus.SUCCESS, all_tests))
        )
        total_tests_failed = len(
            list(filter(lambda x: x.status == TestStatus.FAILED, all_tests))
        )
        return Stats(total_tests, total_tests_succeded, total_tests_failed)
