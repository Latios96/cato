from typing import Optional, Set, Dict, List

from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.test_result import TestResult
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.storage.page import PageRequest, Page
from cato_server.domain.test_result_status_information import (
    TestResultStatusInformation,
)
from cato_server.storage.abstract.abstract_repository import AbstractRepository
from cato_server.storage.abstract.test_result_filter_options import (
    TestResultFilterOptions,
)


class TestResultRepository(AbstractRepository[TestResult, int]):
    def find_by_suite_result_and_test_identifier(
        self, suite_result_id: int, test_identifier: TestIdentifier
    ) -> Optional[TestResult]:
        raise NotImplementedError()

    def find_by_suite_result_id(self, suite_result_id: int) -> List[TestResult]:
        raise NotImplementedError()

    def find_by_run_id(
        self, run_id: int, filter_options: Optional[TestResultFilterOptions] = None
    ) -> List[TestResult]:
        raise NotImplementedError()

    def find_by_run_id_with_paging(
        self,
        run_id: int,
        page_request: PageRequest,
        filter_options: Optional[TestResultFilterOptions] = None,
    ) -> Page[TestResult]:
        raise NotImplementedError()

    def find_by_run_id_and_test_identifier(
        self, run_id: int, test_identifier: TestIdentifier
    ) -> Optional[TestResult]:
        raise NotImplementedError()

    def find_status_by_run_ids(
        self, run_ids: Set[int]
    ) -> Dict[int, Set[UnifiedTestStatus]]:
        raise NotImplementedError()

    def find_status_by_project_id(
        self, project_id: int
    ) -> Dict[int, Set[UnifiedTestStatus]]:
        raise NotImplementedError()

    def test_count_by_run_id(self, run_id: int) -> int:
        raise NotImplementedError()

    def duration_by_run_id(self, run_id: int) -> float:
        raise NotImplementedError()

    def duration_by_run_ids(self, run_ids: Set[int]) -> Dict[int, float]:
        raise NotImplementedError()

    def find_status_by_suite_ids(
        self, suite_ids: Set[int]
    ) -> Dict[int, Set[UnifiedTestStatus]]:
        raise NotImplementedError()

    def find_by_run_id_filter_by_test_status(
        self, run_id: int, test_status: ResultStatus
    ) -> List[TestResult]:
        raise NotImplementedError()

    def status_information_by_run_id(self, run_id: int) -> TestResultStatusInformation:
        raise NotImplementedError()
