from typing import List

import emoji

from cato_common.domain.test_suite_execution_result import TestSuiteExecutionResult
from cato.reporter.stats_calculator import StatsCalculator


class EndMessageGenerator:
    def __init__(self, stats_calculator: StatsCalculator):
        self._stats_calculator = stats_calculator

    def generate_end_message(
        self, result: List[TestSuiteExecutionResult], total_time: float
    ) -> str:

        stats = self._stats_calculator.calculate(result)

        end_message = """Result:
Ran {} tests""".format(
            stats.num_tests
        )

        if stats.succeded_tests:
            end_message += """
{}  succeded :white_check_mark:""".format(
                stats.succeded_tests
            )

        if stats.failed_tests:
            end_message += """
{}  failed   :x:""".format(
                stats.failed_tests
            )

        end_message += f"""
Command execution took {total_time:.1f}s"""

        return emoji.emojize(end_message, language="alias")
