import datetime
from dataclasses import dataclass, field
from typing import List

from cato_common.domain.run import Run
from cato_common.domain.run_batch_identifier import RunBatchIdentifier


@dataclass
class RunBatch:
    id: int
    run_batch_identifier: RunBatchIdentifier
    project_id: int
    created_at: datetime.datetime
    runs: List[Run] = field(default_factory=list)
