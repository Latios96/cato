from typing import Optional, Iterable

from cato_server.storage.abstract.abstract_repository import AbstractRepository
from cato.domain.suite_result import SuiteResult


class SuiteResultRepository(AbstractRepository):
    def save(self, run: SuiteResult) -> SuiteResult:
        raise NotImplementedError()

    def find_by_id(self, id: int) -> Optional[SuiteResult]:
        raise NotImplementedError()

    def find_by_run_id_and_name(self, run_id: int, name: str) -> Optional[SuiteResult]:
        raise NotImplementedError()

    def find_by_run_id(self, run_id: int) -> Iterable[SuiteResult]:
        raise NotImplementedError()
