import logging
from http.client import BAD_REQUEST

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from cato_common.domain.output import Output
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.dtos.finish_test_result_dto import FinishTestResultDto
from cato_common.dtos.start_test_result_dto import StartTestResultDto
from cato_common.dtos.test_result_dto import TestResultDto
from cato_common.dtos.test_result_short_summary_dto import TestResultShortSummaryDto
from cato_common.mappers.object_mapper import ObjectMapper
from cato_common.mappers.page_mapper import PageMapper
from cato_common.storage.page import PageRequest
from cato_common.dtos.api_success import ApiSuccess
from cato_server.api.filter_option_utils import result_filter_options_from_request
from cato_server.api.page_utils import page_request_from_request
from cato_server.api.validators.test_result_validators import (
    CreateOutputValidator,
    FinishTestResultValidator,
    StartTestResultValidator,
)
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.output_repository import OutputRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.abstract.test_result_filter_options import (
    TestResultFilterOptions,
)
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)
from cato_server.usecases.finish_test import FinishTest
from cato_server.usecases.start_test import StartTest

logger = logging.getLogger(__name__)


class TestResultsBlueprint(APIRouter):
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        suite_result_repository: SuiteResultRepository,
        file_storage: AbstractFileStorage,
        output_repository: OutputRepository,
        image_repository: ImageRepository,
        finish_test: FinishTest,
        start_test: StartTest,
        object_mapper: ObjectMapper,
        page_mapper: PageMapper,
    ):
        super(TestResultsBlueprint, self).__init__()
        self._test_result_repository = test_result_repository
        self._suite_result_repository = suite_result_repository
        self._file_storage = file_storage
        self._output_repository = output_repository
        self._image_repository = image_repository
        self._finish_test = finish_test
        self._start_test = start_test
        self._object_mapper = object_mapper
        self._page_mapper = page_mapper

        self.get(
            "/test_results/suite_result/{suite_result_id}/{suite_name}/{test_name}",
        )(self.get_test_result_by_suite_and_identifier)
        self.get(
            "/test_results/runs/{run_id}/{suite_name}/{test_name}",
        )(self.get_test_result_by_run_id_and_identifier)
        self.get("/test_results/suite_result/{suite_id}")(
            self.get_test_result_by_suite_id
        )
        self.get("/test_results/{test_result_id}/output")(self.get_test_result_output)
        self.post("/test_results/output")(self.create_test_result_output)
        self.get("/test_results/run/{run_id}")(self.get_test_result_by_run_id)

        self.get("/test_results/run/{run_id}/test_status/{test_status}")(
            self.get_test_result_by_run_id_and_test_status
        )

        self.get("/test_results/{test_result_id}")(self.get_test_result_by_id)
        self.post("/test_results/finish")(self.finish_test_result)
        self.post("/test_results/start")(self.start_test_result)

    def get_test_result_by_suite_and_identifier(
        self, suite_result_id: int, suite_name: str, test_name: str
    ) -> Response:
        identifier = TestIdentifier(suite_name, test_name)
        test_result = (
            self._test_result_repository.find_by_suite_result_and_test_identifier(
                suite_result_id, identifier
            )
        )
        if not test_result:
            return Response(status_code=404)

        return JSONResponse(
            content=self._object_mapper.to_dict(test_result), status_code=200
        )

    def get_test_result_by_run_id_and_identifier(
        self, run_id: int, suite_name: str, test_name: str
    ) -> Response:
        identifier = TestIdentifier(suite_name, test_name)
        suite_result = self._suite_result_repository.find_by_run_id_and_name(
            run_id, suite_name
        )
        if not suite_result:
            return Response(status_code=404)

        test_result = (
            self._test_result_repository.find_by_suite_result_and_test_identifier(
                suite_result.id, identifier
            )
        )
        if not test_result:
            return Response(status_code=404)

        return JSONResponse(content=self._object_mapper.to_dict(test_result))

    def get_test_result_by_suite_id(self, suite_id: int) -> Response:
        test_results = self._test_result_repository.find_by_suite_result_id(suite_id)
        return JSONResponse(content=self._object_mapper.many_to_dict(test_results))

    def get_test_result_output(self, test_result_id: int) -> Response:
        output = self._output_repository.find_by_test_result_id(test_result_id)
        if not output:
            return Response(status_code=404)
        return JSONResponse(content=self._object_mapper.to_dict(output))

    async def create_test_result_output(self, request: Request) -> Response:
        request_json = await request.json()
        errors = CreateOutputValidator(
            self._test_result_repository, self._output_repository
        ).validate(request_json)
        if errors:
            return JSONResponse(content=errors, status_code=BAD_REQUEST)

        output = self._object_mapper.from_dict(request_json, Output)
        output = self._output_repository.save(output)
        logger.info(
            "Saved output with id %s for test result with id %s",
            output.id,
            output.test_result_id,
        )
        return JSONResponse(
            content=self._object_mapper.to_dict(output), status_code=201
        )

    def get_test_result_by_run_id(self, run_id: int, request: Request) -> Response:
        page_request = page_request_from_request(request.query_params)
        filter_options = result_filter_options_from_request(request.query_params)
        if page_request:
            return self._get_test_result_by_run_id_paged(
                run_id, page_request, filter_options
            )

        test_results = self._test_result_repository.find_by_run_id(
            run_id, filter_options
        )

        test_result_short_summary_dtos = []
        for test_result in test_results:
            test_result_short_summary_dtos.append(
                TestResultShortSummaryDto(
                    id=test_result.id,
                    name=test_result.test_name,
                    test_identifier=test_result.test_identifier,
                    unified_test_status=test_result.unified_test_status,
                    thumbnail_file_id=test_result.thumbnail_file_id,
                    seconds=test_result.seconds,
                )
            )
        return JSONResponse(
            content=self._object_mapper.many_to_dict(test_result_short_summary_dtos)
        )

    def _get_test_result_by_run_id_paged(
        self,
        run_id: int,
        page_request: PageRequest,
        filter_options: TestResultFilterOptions,
    ) -> Response:
        page = self._test_result_repository.find_by_run_id_with_paging(
            run_id, page_request, filter_options
        )

        test_result_short_summary_dtos = []
        for test_result in page.entities:
            test_result_short_summary_dtos.append(
                TestResultShortSummaryDto(
                    id=test_result.id,
                    name=test_result.test_name,
                    test_identifier=test_result.test_identifier,
                    unified_test_status=test_result.unified_test_status,
                    thumbnail_file_id=test_result.thumbnail_file_id,
                    seconds=test_result.seconds,
                )
            )
        page.entities = test_result_short_summary_dtos
        return JSONResponse(content=self._page_mapper.to_dict(page))

    def get_test_result_by_id(self, test_result_id) -> Response:
        result = self._test_result_repository.find_by_id(test_result_id)
        if not result:
            return Response(status_code=404)

        test_result_dto = TestResultDto(
            id=result.id,
            suite_result_id=result.suite_result_id,
            test_name=result.test_name,
            test_identifier=result.test_identifier,
            test_command=result.test_command,
            test_variables=result.test_variables,
            machine_info=result.machine_info,
            unified_test_status=result.unified_test_status,
            seconds=result.seconds if result.seconds is not None else 0,
            message=result.message if result.message else None,
            image_output=self._image_repository.find_by_id(result.image_output),
            reference_image=self._image_repository.find_by_id(result.reference_image),
            diff_image=self._image_repository.find_by_id(result.diff_image),
            started_at=result.started_at,
            finished_at=result.finished_at,
            comparison_settings=result.comparison_settings,
            error_value=result.error_value,
            thumbnail_file_id=result.thumbnail_file_id,
        )
        return JSONResponse(content=self._object_mapper.to_dict(test_result_dto))

    async def finish_test_result(self, request: Request) -> Response:
        request_json = await request.json()
        errors = FinishTestResultValidator(
            self._test_result_repository, self._image_repository
        ).validate(request_json)
        if errors:
            return JSONResponse(content=errors, status_code=BAD_REQUEST)

        finish_test_result_dto = self._object_mapper.from_dict(
            request_json, FinishTestResultDto
        )

        self._finish_test.finish_test(
            finish_test_result_dto.id,
            ResultStatus(finish_test_result_dto.status.value),
            finish_test_result_dto.seconds,
            finish_test_result_dto.message,
            finish_test_result_dto.image_output,
            finish_test_result_dto.reference_image,
            finish_test_result_dto.diff_image,
            finish_test_result_dto.error_value,
            finish_test_result_dto.failure_reason,
        )
        return JSONResponse(content=self._object_mapper.to_dict(ApiSuccess.ok()))

    async def start_test_result(self, request: Request) -> Response:
        request_json = await request.json()
        errors = StartTestResultValidator(self._test_result_repository).validate(
            request_json
        )
        if errors:
            return JSONResponse(content=errors, status_code=BAD_REQUEST)

        start_test_result_dto = self._object_mapper.from_dict(
            request_json, StartTestResultDto
        )

        self._start_test.start_test(
            start_test_result_dto.id, start_test_result_dto.machine_info
        )

        return JSONResponse(content=self._object_mapper.to_dict(ApiSuccess.ok()))

    def get_test_result_by_run_id_and_test_status(
        self, run_id: int, test_status: str
    ) -> Response:
        try:
            test_status = UnifiedTestStatus(test_status)
        except ValueError:
            return JSONResponse(
                content={"test_status": f"Not a valid test status: {test_status}."},
                status_code=400,
            )
        test_results = (
            self._test_result_repository.find_by_run_id_filter_by_test_status(
                run_id, test_status
            )
        )

        test_identifiers = list(map(lambda x: x.test_identifier, test_results))

        return JSONResponse(content=self._object_mapper.many_to_dict(test_identifiers))
