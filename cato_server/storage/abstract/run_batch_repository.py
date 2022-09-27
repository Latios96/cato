from typing import Optional, Callable

from cato_common.domain.run_batch_identifier import RunBatchIdentifier
from cato_common.storage.page import PageRequest, Page
from cato_server.domain.run_batch import RunBatch
from cato_server.storage.abstract.abstract_repository import AbstractRepository
from cato_server.storage.abstract.run_filter_options import RunFilterOptions


class RunBatchRepository(AbstractRepository[RunBatch, int]):
    def find_by_project_id_and_run_batch_identifier(
        self, project_id: int, run_batch_identifier: RunBatchIdentifier
    ) -> Optional[RunBatch]:
        raise NotImplementedError()

    def find_or_save_by_project_id_and_run_batch_identifier(
        self,
        project_id: int,
        run_batch_identifier: RunBatchIdentifier,
        run_batch_factory: Callable[[], RunBatch],
    ) -> RunBatch:
        raise NotImplementedError()

    def find_by_project_id_with_paging(
        self,
        id: int,
        page_request: PageRequest,
        filter_options: Optional[RunFilterOptions] = None,
    ) -> Page[RunBatch]:
        raise NotImplementedError()
