from collections import defaultdict
from typing import Set, Dict

from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_server.domain.run_status import RunStatus


class RunStatusCalculator:
    def calculate(self, status_set: Set[UnifiedTestStatus]) -> RunStatus:
        status_counts: Dict[UnifiedTestStatus, int] = defaultdict(lambda: 0)

        for execution_status in status_set:
            status_counts[execution_status] += 1

        total = len(status_set)

        if status_counts[UnifiedTestStatus.NOT_STARTED] == total:
            return RunStatus.NOT_STARTED
        elif (
            status_counts[UnifiedTestStatus.NOT_STARTED] == 0
            and status_counts[UnifiedTestStatus.RUNNING] == 0
        ):
            if status_counts[UnifiedTestStatus.FAILED] > 0:
                return RunStatus.FAILED
            else:
                return RunStatus.SUCCESS
        elif status_counts[UnifiedTestStatus.RUNNING] > 0:
            return RunStatus.RUNNING
        else:
            return RunStatus.NOT_STARTED
