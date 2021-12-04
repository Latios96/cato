from dataclasses import dataclass
from typing import Set

from cato_common.domain.branch_name import BranchName


@dataclass
class RunFilterOptions:
    branches: Set[BranchName]
