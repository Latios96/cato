from typing import List

from cato_common.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.reporter.stats_calculator import StatsCalculator


class ExitCodeCalculator:
    def __init__(self, stats_calculator: StatsCalculator):
        self._stats_calculator = stats_calculator

    def generate_exit_code(self, result: List[TestSuiteExecutionResult]) -> int:
        stats = self._stats_calculator.calculate(result)

        if stats.failed_tests > 0:
            return 1
        return 0
