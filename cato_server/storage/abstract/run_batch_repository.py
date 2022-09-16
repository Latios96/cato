from typing import Optional

from cato_common.domain.run_batch_identifier import RunBatchIdentifier
from cato_server.domain.run_batch import RunBatch
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class RunBatchRepository(AbstractRepository[RunBatch, int]):
    def find_by_run_batch_identifier(
        self, run_batch_identifier: RunBatchIdentifier
    ) -> Optional[RunBatch]:
        raise NotImplementedError()
