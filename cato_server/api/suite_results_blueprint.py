import logging
from http.client import BAD_REQUEST

from fastapi import APIRouter
from marshmallow import ValidationError
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from cato_api_models.catoapimodels import (
    SuiteResultDto,
    SuiteStatusDto,
    SuiteResultSummaryDto,
    TestResultShortSummaryDto,
    ExecutionStatusDto,
    TestStatusDto,
)
from cato_server.api.page_utils import page_request_from_request
from cato_server.api.validators.suite_result_validators import (
    CreateSuiteResultValidator,
)
from cato_server.domain.suite_result import SuiteResult
from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.mappers.page_mapper import PageMapper
from cato_server.run_status_calculator import RunStatusCalculator
from cato_server.storage.abstract.page import PageRequest, Page
from cato_server.storage.abstract.run_repository import RunRepository
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

        self.get("/suite_results/run/{run_id}")(self.suite_result_by_run)
        self.get("/suite_results/{suite_id}")(self.suite_result_by_id)
        self.post("/suite_results")(self.create_suite_result)

    def suite_result_by_run(self, run_id: int, request: Request) -> Response:
        page_request = page_request_from_request(request.query_params)
        if page_request:
            return self._suite_result_by_run_paged(run_id, page_request)
        suite_results = self._suite_result_repository.find_by_run_id(run_id)

        status_by_suite_id = (
            self._test_result_repository.find_execution_status_by_suite_ids(
                set(map(lambda x: x.id, suite_results))
            )
        )

        suite_result_dtos = []
        for suite_result in suite_results:
            suite_result_dtos.append(
                SuiteResultDto(
                    id=suite_result.id,
                    run_id=suite_result.run_id,
                    suite_name=suite_result.suite_name,
                    suite_variables=suite_result.suite_variables,
                    status=SuiteStatusDto(
                        self._status_calculator.calculate(
                            status_by_suite_id.get(suite_result.id, set())
                        ).value
                    ),
                )
            )
        return JSONResponse(content=self._object_mapper.many_to_dict(suite_result_dtos))

    def _suite_result_by_run_paged(
        self, run_id: int, page_request: PageRequest
    ) -> Response:
        suite_results_page = self._suite_result_repository.find_by_run_id_with_paging(
            run_id, page_request
        )

        status_by_suite_id = (
            self._test_result_repository.find_execution_status_by_suite_ids(
                set(map(lambda x: x.id, suite_results_page.entities))
            )
        )

        suite_result_dtos = []
        for suite_result in suite_results_page.entities:
            suite_result_dtos.append(
                SuiteResultDto(
                    id=suite_result.id,
                    run_id=suite_result.run_id,
                    suite_name=suite_result.suite_name,
                    suite_variables=suite_result.suite_variables,
                    status=SuiteStatusDto(
                        self._status_calculator.calculate(
                            status_by_suite_id.get(suite_result.id, set())
                        ).value
                    ),
                )
            )
        page = Page(
            page_number=page_request.page_number,
            page_size=page_request.page_size,
            total_entity_count=suite_results_page.total_entity_count,
            entities=suite_result_dtos,
        )
        return JSONResponse(content=self._page_mapper.to_dict(page))

    async def create_suite_result(self, request: Request) -> Response:
        request_json = await request.json()
        errors = CreateSuiteResultValidator(
            self._run_repository, self._suite_result_repository
        ).validate(request_json)
        if errors:
            return JSONResponse(content=errors, status_code=BAD_REQUEST)

        suite_result = SuiteResult(
            id=0,
            run_id=request_json["run_id"],
            suite_name=request_json["suite_name"],
            suite_variables=request_json["suite_variables"],
        )
        suite_result = self._suite_result_repository.save(suite_result)
        logger.info("Created SuiteResult %s", suite_result)
        return JSONResponse(
            content=self._object_mapper.to_dict(suite_result), status_code=201
        )

    def _run_id_exists(self, id):
        if self._run_repository.find_by_id(id) is None:
            raise ValidationError(f"No run with id {id} exists.")

    def _is_str_str_dict(self, the_dict):
        for key, value in the_dict.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValidationError(f"Not a mapping of str->str: {key}={value}")

    def suite_result_by_id(self, suite_id):
        suite_result = self._suite_result_repository.find_by_id(suite_id)
        if not suite_result:
            return Response(status_code=404)

        tests = self._test_result_repository.find_by_suite_result_id(suite_id)
        tests_result_short_summary_dtos = []
        for test in tests:
            tests_result_short_summary_dtos.append(
                TestResultShortSummaryDto(
                    id=test.id,
                    name=test.test_name,
                    test_identifier=str(test.test_identifier),
                    execution_status=ExecutionStatusDto(test.execution_status.value),
                    status=TestStatusDto(
                        test.status.value if test.status else "FAILED"
                    ),
                )
            )

        dto = SuiteResultSummaryDto(
            id=suite_result.id,
            run_id=suite_result.run_id,
            suite_name=suite_result.suite_name,
            suite_variables=suite_result.suite_variables,
            tests=tests_result_short_summary_dtos,
        )
        return JSONResponse(content=self._object_mapper.to_dict(dto))
