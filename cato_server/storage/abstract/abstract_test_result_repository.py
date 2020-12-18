from typing import Optional, Iterable, Set, Tuple, Dict

from cato.domain.test_status import TestStatus
from cato_server.domain.execution_status import ExecutionStatus
from cato_server.domain.test_identifier import TestIdentifier
from cato_server.domain.test_result import TestResult
from cato_server.storage.abstract.abstract_repository import AbstractRepository


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

    def find_by_run_id(self, run_id: int) -> Iterable[TestResult]:
        raise NotImplementedError()

    def find_execution_status_by_run_ids(
        self, run_ids: Set[int]
    ) -> Dict[int, Set[Tuple[ExecutionStatus, TestStatus]]]:
        raise NotImplementedError()

    def find_execution_status_by_project_id(
        self, project_id: int
    ) -> Dict[int, Set[Tuple[ExecutionStatus, TestStatus]]]:
        raise NotImplementedError()

    def test_count_by_run_id(self, run_id: int) -> int:
        raise NotImplementedError()

    def failed_test_count_by_run_id(self, run_id: int) -> int:
        raise NotImplementedError()

    def duration_by_run_id(self, run_id: int) -> float:
        raise NotImplementedError()
