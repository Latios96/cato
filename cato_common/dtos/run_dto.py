from dataclasses import dataclass
from datetime import datetime

from cato_common.domain.branch_name import BranchName
from cato_common.domain.run_information import BasicRunInformation
from cato_server.domain.run_status import RunStatus


@dataclass
class RunDto:
    id: int
    project_id: int
    started_at: datetime
    status: RunStatus
    duration: float
    branch_name: BranchName
    run_information: BasicRunInformation
