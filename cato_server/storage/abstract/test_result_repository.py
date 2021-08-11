from typing import Optional, Set, Tuple, Dict, List

from cato.domain.test_status import TestStatus
from cato_common.domain.execution_status import ExecutionStatus
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.test_result import TestResult
from cato_server.storage.abstract.abstract_repository import AbstractRepository
from cato_common.storage.page import PageRequest, Page


class TestResultRepository(AbstractRepository[TestResult, int]):
    def find_by_suite_result_and_test_identifier(
        self, suite_result_id: int, test_identifier: TestIdentifier
    ) -> Optional[TestResult]:
        raise NotImplementedError()

    def find_by_suite_result_id(self, suite_result_id: int) -> List[TestResult]:
        raise NotImplementedError()

    def find_by_run_id(self, run_id: int) -> List[TestResult]:
        raise NotImplementedError()

    def find_by_run_id_with_paging(
        self, run_id: int, page_request: PageRequest
    ) -> Page[TestResult]:
        raise NotImplementedError()

    def find_by_run_id_and_test_identifier(
        self, run_id: int, test_identifier: TestIdentifier
    ) -> Optional[TestResult]:
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

    def duration_by_run_ids(self, run_ids: Set[int]) -> Dict[int, float]:
        raise NotImplementedError()

    def find_execution_status_by_suite_ids(
        self, suite_ids: Set[int]
    ) -> Dict[int, Set[Tuple[ExecutionStatus, TestStatus]]]:
        raise NotImplementedError()

    def find_by_run_id_filter_by_test_status(
        self, run_id: int, test_status: TestStatus
    ) -> List[TestResult]:
        raise NotImplementedError()
