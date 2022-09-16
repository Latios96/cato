from dataclasses import dataclass

from cato_common.domain.run_batch_identifier import RunBatchIdentifier


@dataclass
class RunBatch:
    id: int
    run_batch_identifier: RunBatchIdentifier
    project_id: int
