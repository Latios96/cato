from dataclasses import dataclass
from typing import List

from cato_common.domain.run import Run
from cato_common.domain.run_batch_identifier import RunBatchIdentifier


@dataclass
class RunBatch:
    id: int
    batch_identifier: RunBatchIdentifier
    project_id: int
    runs: List[Run]
