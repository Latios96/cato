import itertools

import emoji

from cato.domain.test_result import TestStatus
from cato.domain.test_suite_execution_result import TestSuiteExecutionResult


class EndMessageGenerator:
    def generate_end_message(self, result: TestSuiteExecutionResult) -> str:

        all_tests = list(itertools.chain(*map(lambda x: x.test_results, result)))

        total_tests = len(all_tests)
        total_tests_succeded = len(
            list(filter(lambda x: x.result == TestStatus.SUCCESS, all_tests))
        )
        total_tests_failed = len(
            list(filter(lambda x: x.result == TestStatus.FAILED, all_tests))
        )

        return emoji.emojize(
            """Result:
Ran {} tests
{}  succeded :white_check_mark:
{}  failed   :x:""".format(
                total_tests, total_tests_succeded, total_tests_failed
            ),
            use_aliases=True,
        )
