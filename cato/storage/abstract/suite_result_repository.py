from typing import Optional

from cato.storage.abstract.abstract_repository import AbstractRepository
from cato.storage.domain.suite_result import SuiteResult


class SuiteResultRepository(AbstractRepository):
    def save(self, run: SuiteResult) -> SuiteResult:
        raise NotImplementedError()

    def find_by_id(self, id: int) -> Optional[SuiteResult]:
        pass
