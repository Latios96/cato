from typing import Optional, Iterable

from cato.domain.test_identifier import TestIdentifier
from cato_server.storage.abstract.abstract_repository import AbstractRepository
from cato.domain.test_result import TestResult


class TestResultRepository(AbstractRepository):
    def save(self, run: TestResult) -> TestResult:
        raise NotImplementedError()

    def find_by_id(self, id: int) -> Optional[TestResult]:
        raise NotImplementedError()

    def find_by_suite_result_and_test_identifier(
        self, suite_result_id: int, test_identifier: TestIdentifier
    ) -> Optional[TestResult]:
        raise NotImplementedError()

    def find_by_suite_result(self, suite_result_id: int) -> Iterable[TestResult]:
        raise NotImplementedError()
