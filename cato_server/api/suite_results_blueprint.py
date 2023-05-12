import logging
from collections import defaultdict
from typing import DefaultDict, List, Set

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from cato_common.domain.test_result import TestResult
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.dtos.suite_result_summary_dto import SuiteResultSummaryDto
from cato_common.dtos.test_result_short_summary_dto import TestResultShortSummaryDto
from cato_common.mappers.object_mapper import ObjectMapper
from cato_common.mappers.page_mapper import PageMapper
from cato_server.api.filter_option_utils import suite_result_filter_options_from_request
from cato_server.domain.run_status import RunStatus
from cato_server.run_status_calculator import RunStatusCalculator
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.status_filter import StatusFilter
from cato_server.storage.abstract.suite_result_filter_options import (
    SuiteResultFilterOptions,
)
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)

logger = logging.getLogger(__name__)


def run_id_exists(self, id):
    return self._run_repository.find_by_id(id) is not None


class SuiteResultsBlueprint(APIRouter):
    def __init__(
        self,
        suite_result_repository: SuiteResultRepository,
        run_repository: RunRepository,
        test_result_repository: TestResultRepository,
        object_mapper: ObjectMapper,
        page_mapper: PageMapper,
    ):
        super(SuiteResultsBlueprint, self).__init__()
        self._suite_result_repository = suite_result_repository
        self._run_repository = run_repository
        self._test_result_repository = test_result_repository
        self._object_mapper = object_mapper
        self._page_mapper = page_mapper

        self._status_calculator = RunStatusCalculator()

        self.get("/suite_results/run/{run_id}")(self.suite_result_by_run_id)

    def suite_result_by_run_id(self, run_id, request: Request) -> Response:
        filter_options = suite_result_filter_options_from_request(request.query_params)
        suite_results = self._suite_result_repository.find_by_run_id(run_id)

        tests = self._test_result_repository.find_by_run_id(run_id)

        tests_by_suite_result_id: DefaultDict[int, List[TestResult]] = defaultdict(list)
        status_by_suite_id: DefaultDict[int, Set[UnifiedTestStatus]] = defaultdict(set)
        for test in tests:
            tests_by_suite_result_id[test.suite_result_id].append(test)
            status_by_suite_id[test.suite_result_id].add(test.unified_test_status)

        suite_result_dtos = []
        for suite_result in suite_results:
            status = self._status_calculator.calculate(
                status_by_suite_id.get(suite_result.id, set())
            )
            if _is_filtered(filter_options, status):
                continue
            tests = tests_by_suite_result_id.get(suite_result.id, [])
            tests_result_short_summary_dtos = []
            for test in tests:
                tests_result_short_summary_dtos.append(
                    TestResultShortSummaryDto(
                        id=test.id,
                        name=test.test_name,
                        test_identifier=test.test_identifier,
                        unified_test_status=test.unified_test_status,
                        thumbnail_file_id=test.thumbnail_file_id,
                        seconds=test.seconds,
                    )
                )
            dto = SuiteResultSummaryDto(
                id=suite_result.id,
                run_id=suite_result.run_id,
                suite_name=suite_result.suite_name,
                suite_variables=suite_result.suite_variables,
                tests=tests_result_short_summary_dtos,
                status=status,
            )
            suite_result_dtos.append(dto)

        return JSONResponse(content=self._object_mapper.many_to_dict(suite_result_dtos))


def _is_filtered(filter_options: SuiteResultFilterOptions, status: RunStatus):
    if filter_options.status == StatusFilter.NONE:
        return False

    if (
        filter_options.status == StatusFilter.NOT_STARTED
        and status == RunStatus.NOT_STARTED
    ):
        return False
    elif filter_options.status == StatusFilter.RUNNING and status == RunStatus.RUNNING:
        return False
    elif filter_options.status == StatusFilter.FAILED and status == RunStatus.FAILED:
        return False
    elif filter_options.status == StatusFilter.SUCCESS and status == RunStatus.SUCCESS:
        return False

    return True
