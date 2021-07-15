from typing import Optional, List

from cato_server.storage.abstract.abstract_repository import AbstractRepository
from cato_server.domain.suite_result import SuiteResult
from cato_server.storage.abstract.page import PageRequest, Page


class SuiteResultRepository(AbstractRepository):
    def find_by_id(self, id: int) -> Optional[SuiteResult]:
        raise NotImplementedError()

    def find_by_run_id_with_paging(
        self, run_id: int, page_request: PageRequest
    ) -> Page[SuiteResult]:
        raise NotImplementedError()

    def find_by_run_id_and_name(self, run_id: int, name: str) -> Optional[SuiteResult]:
        raise NotImplementedError()

    def find_by_run_id(self, run_id: int) -> List[SuiteResult]:
        raise NotImplementedError()

    def suite_count_by_run_id(self, run_id: int) -> int:
        raise NotImplementedError()
