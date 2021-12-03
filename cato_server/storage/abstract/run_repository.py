from typing import List

from cato_common.domain.run import Run
from cato_server.storage.abstract.abstract_repository import AbstractRepository
from cato_common.storage.page import PageRequest, Page


class RunRepository(AbstractRepository[Run, int]):
    def find_by_project_id(self, id: int) -> List[Run]:
        raise NotImplementedError()

    def find_by_project_id_with_paging(
        self, id: int, page_request: PageRequest
    ) -> Page[Run]:
        raise NotImplementedError()

    def find_previous_run_by_branch_name(
        self, project_id: int, branch_name: str
    ) -> Run:
        raise NotImplementedError()
