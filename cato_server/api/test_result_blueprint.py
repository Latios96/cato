import logging
from http.client import BAD_REQUEST
from typing import Optional

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from cato.domain.test_status import TestStatus
from cato_api_models.catoapimodels import (
    TestResultDto,
    ImageDto,
    ImageChannelDto,
    ExecutionStatusDto,
    TestStatusDto,
    MachineInfoDto,
    TestResultShortSummaryDto,
    FinishTestResultDto,
    ApiSuccess,
    StartTestResultDto,
)
from cato_common.mappers.page_mapper import PageMapper

from cato_server.api.page_utils import page_request_from_request
from cato_server.api.validators.test_result_validators import (
    CreateOutputValidator,
    FinishTestResultValidator,
    StartTestResultValidator,
)
from cato_common.domain.image import ImageChannel
from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.output import Output
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.test_result import TestResult
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.output_repository import OutputRepository
from cato_common.storage.page import PageRequest
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
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
        logger.info(
            "Saving output for test result with id %s", request_json["test_result_id"]
        )
        output = self._output_repository.save(output)
        return JSONResponse(
            content=self._object_mapper.to_dict(output), status_code=201
        )

    def get_test_result_by_run_id(self, run_id: int, request: Request) -> Response:
        page_request = page_request_from_request(request.query_params)
        if page_request:
            return self._get_test_result_by_run_id_paged(run_id, page_request)
        test_results = self._test_result_repository.find_by_run_id(run_id)

        test_result_short_summary_dtos = []
        for test_result in test_results:
            test_result_short_summary_dtos.append(
                TestResultShortSummaryDto(
                    id=test_result.id,
                    name=test_result.test_name,
                    test_identifier=str(test_result.test_identifier),
                    execution_status=ExecutionStatusDto(
                        test_result.execution_status.value
                    ),
                    status=TestStatusDto(
                        test_result.status.value
                        if test_result.status
                        else TestStatus.FAILED
                    ),
                )
            )
        return JSONResponse(
            content=self._object_mapper.many_to_dict(test_result_short_summary_dtos)
        )

    def _get_test_result_by_run_id_paged(
        self, run_id: int, page_request: PageRequest
    ) -> Response:
        page = self._test_result_repository.find_by_run_id_with_paging(
            run_id, page_request
        )

        test_result_short_summary_dtos = []
        for test_result in page.entities:
            test_result_short_summary_dtos.append(
                TestResultShortSummaryDto(
                    id=test_result.id,
                    name=test_result.test_name,
                    test_identifier=str(test_result.test_identifier),
                    execution_status=ExecutionStatusDto(
                        test_result.execution_status.value
                    ),
                    status=TestStatusDto(
                        test_result.status.value
                        if test_result.status
                        else TestStatus.FAILED
                    ),
                )
            )
        page.entities = test_result_short_summary_dtos
        return JSONResponse(content=self._page_mapper.to_dict(page))

    def get_test_result_by_id(self, test_result_id) -> Response:
        result = self._test_result_repository.find_by_id(test_result_id)
        if not result:
            return Response(status_code=404)

        image_output_dto = self._map_to_image_dto(result.image_output)
        reference_image_dto = self._map_to_image_dto(result.reference_image)
        diff_image_dto = self._map_to_image_dto(result.diff_image)

        test_result_dto = TestResultDto(
            id=result.id,
            suite_result_id=result.suite_result_id,
            test_name=result.test_name,
            test_identifier=str(result.test_identifier),
            test_command=result.test_command,
            test_variables=result.test_variables,
            machine_info=MachineInfoDto(
                cpu_name=result.machine_info.cpu_name,
                cores=result.machine_info.cores,
                memory=result.machine_info.memory,
            )
            if result.machine_info
            else None,
            execution_status=ExecutionStatusDto(result.execution_status.value),
            status=TestStatusDto(result.status.value) if result.status else None,
            seconds=result.seconds if result.seconds is not None else 0,
            message=result.message if result.message else None,
            image_output=image_output_dto,
            reference_image=reference_image_dto,
            diff_image=diff_image_dto,
            started_at=result.started_at.isoformat() if result.started_at else None,
            finished_at=result.finished_at.isoformat() if result.finished_at else None,
        )
        return JSONResponse(content=self._object_mapper.to_dict(test_result_dto))

    def _map_to_image_dto(self, image_output) -> Optional[ImageDto]:
        image = self._image_repository.find_by_id(image_output)
        if image:
            return ImageDto(
                id=image.id,
                name=image.name,
                original_file_id=image.original_file_id,
                channels=list(map(self._to_channel_dto, image.channels)),
                width=image.width,
                height=image.height,
            )

    def _to_channel_dto(self, channel: ImageChannel) -> ImageChannelDto:
        return ImageChannelDto(
            id=channel.id, name=channel.name, file_id=channel.file_id
        )

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
            TestStatus(finish_test_result_dto.status.value),
            finish_test_result_dto.seconds,
            finish_test_result_dto.message,
            finish_test_result_dto.image_output,
            finish_test_result_dto.reference_image,
            finish_test_result_dto.diff_image,
        )
        return JSONResponse(
            content=self._object_mapper.to_dict(ApiSuccess(success=True))
        )

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

        machine_info_dto = start_test_result_dto.machine_info
        machine_info = MachineInfo(
            cpu_name=machine_info_dto.cpu_name,
            cores=machine_info_dto.cores,
            memory=machine_info_dto.memory,
        )
        self._start_test.start_test(start_test_result_dto.id, machine_info)

        return JSONResponse(
            content=self._object_mapper.to_dict(ApiSuccess(success=True))
        )

    def get_test_result_by_run_id_and_test_status(
        self, run_id, test_status
    ) -> Response:
        try:
            test_status = TestStatus(test_status)
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
