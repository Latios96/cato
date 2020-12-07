from collections import defaultdict
from typing import List

from cato.domain.execution_status import ExecutionStatus
from cato.domain.run_status import RunStatus
from cato.domain.test_result import TestResult
from cato.domain.test_status import TestStatus


class RunStatusCalculator:
    def calculate(self, test_results: List[TestResult]) -> RunStatus:
        execution_status_counts = defaultdict(lambda: 0)
        test_status_counts = defaultdict(lambda: 0)

        for result in test_results:
            execution_status_counts[result.execution_status] += 1
            test_status_counts[result.status] += 1

        total = len(test_results)

        print(test_results)

        if execution_status_counts[ExecutionStatus.NOT_STARTED] == total:
            return RunStatus.NOT_STARTED
        elif execution_status_counts[ExecutionStatus.FINISHED] == total:
            if test_status_counts[TestStatus.FAILED] > 0:
                return RunStatus.FAILED
            else:
                return RunStatus.SUCCESS
        else:
            return RunStatus.RUNNING
