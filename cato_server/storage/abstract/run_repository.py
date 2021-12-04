from typing import List, Optional

from cato_common.domain.branch_name import BranchName
from cato_common.domain.run import Run
from cato_server.storage.abstract.abstract_repository import AbstractRepository
from cato_common.storage.page import PageRequest, Page
from cato_server.storage.abstract.run_filter_options import RunFilterOptions


class RunRepository(AbstractRepository[Run, int]):
    def find_by_project_id(self, id: int) -> List[Run]:
        raise NotImplementedError()  # todo clean this up

    def find_by_project_id_with_paging(
        self,
        id: int,
        page_request: PageRequest,
        filter_options: Optional[RunFilterOptions] = None,
    ) -> Page[Run]:
        raise NotImplementedError()

    def find_last_run_for_project(
        self, project_id: int, branch_name: BranchName
    ) -> Optional[Run]:
        raise NotImplementedError()
