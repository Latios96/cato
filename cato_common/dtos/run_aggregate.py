from dataclasses import dataclass
from datetime import datetime

from cato_common.domain.branch_name import BranchName
from cato_common.domain.run_information import BasicRunInformation
from cato_server.domain.run_status import RunStatus


@dataclass
class RunProgress:
    waiting_test_count: int
    running_test_count: int
    failed_test_count: int
    succeeded_test_count: int
    progress_percentage: float


@dataclass
class RunAggregate:
    id: int
    project_id: int
    created_at: datetime
    status: RunStatus
    duration: float
    branch_name: BranchName
    run_information: BasicRunInformation
    suite_count: int
    test_count: int
    progress: RunProgress
