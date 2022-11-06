from dataclasses import dataclass
import datetime
from typing import Optional

from cato_common.domain.branch_name import BranchName
from cato_common.domain.run_information import BasicRunInformation


@dataclass
class Run:
    id: int
    project_id: int
    run_batch_id: int
    created_at: datetime.datetime
    branch_name: BranchName
    previous_run_id: Optional[int]
    run_information: BasicRunInformation
