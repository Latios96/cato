import datetime
from dataclasses import dataclass
from typing import List

from cato_common.domain.branch_name import BranchName
from cato_common.domain.run_batch_identifier import RunBatchIdentifier
from cato_common.dtos.run_aggregate import RunAggregate, RunProgress
from cato_server.domain.run_status import RunStatus


@dataclass
class RunBatchAggregate:
    id: int
    run_batch_identifier: RunBatchIdentifier
    project_id: int
    created_at: datetime.datetime
    runs: List[RunAggregate]
    status: RunStatus
    duration: float
    branch_name: BranchName
    suite_count: int
    test_count: int
    progress: RunProgress
