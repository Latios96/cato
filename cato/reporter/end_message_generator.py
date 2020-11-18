from typing import List

import emoji

from cato.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.reporter.stats_calculator import StatsCalculator


class EndMessageGenerator:
    def __init__(self, stats_calculator: StatsCalculator):
        self._stats_calculator = stats_calculator

    def generate_end_message(self, result: List[TestSuiteExecutionResult]) -> str:

        stats = self._stats_calculator.calculate(result)

        return emoji.emojize(
            """Result:
Ran {} tests
{}  succeded :white_check_mark:
{}  failed   :x:""".format(
                stats.num_tests, stats.succeded_tests, stats.failed_tests
            ),
            use_aliases=True,
        )
