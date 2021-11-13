from collections import defaultdict
from typing import Set, Tuple, Dict

from cato_common.domain.test_status import TestStatus
from cato_common.domain.execution_status import ExecutionStatus
from cato_server.domain.run_status import RunStatus


class RunStatusCalculator:
    def calculate(
        self, status_set: Set[Tuple[ExecutionStatus, TestStatus]]
    ) -> RunStatus:
        execution_status_counts: Dict[ExecutionStatus, int] = defaultdict(lambda: 0)
        test_status_counts: Dict[TestStatus, int] = defaultdict(lambda: 0)

        for execution_status, test_status in status_set:
            execution_status_counts[execution_status] += 1
            test_status_counts[test_status] += 1

        total = len(status_set)

        if execution_status_counts[ExecutionStatus.NOT_STARTED] == total:
            return RunStatus.NOT_STARTED
        elif execution_status_counts[ExecutionStatus.FINISHED] == total:
            if test_status_counts[TestStatus.FAILED] > 0:
                return RunStatus.FAILED
            else:
                return RunStatus.SUCCESS
        elif execution_status_counts[ExecutionStatus.RUNNING] > 0:
            return RunStatus.RUNNING
        else:
            return RunStatus.NOT_STARTED
