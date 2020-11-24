from typing import Optional

from cato.domain.test_identifier import TestIdentifier
from cato.storage.abstract.abstract_repository import AbstractRepository
from cato.storage.domain.test_result import TestResult


class AbstractTestResultRepository(AbstractRepository):
    def save(self, run: TestResult) -> TestResult:
        raise NotImplementedError()

    def find_by_id(self, id: int) -> Optional[TestResult]:
        raise NotImplementedError()

    def find_by_test_identifier(self, test_identifier: TestIdentifier):
        raise NotImplementedError()
