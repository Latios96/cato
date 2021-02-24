import logging
from http.client import BAD_REQUEST

from flask import jsonify, abort, request

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
)
from cato_server.api.base_blueprint import BaseBlueprint
from cato_server.api.page_utils import page_request_from_request
from cato_server.api.schemas.test_result_schemas import UpdateTestResultSchema
from cato_server.api.validators.test_result_validators import (
    CreateTestResultValidator,
    UpdateTestResultValidator,
    CreateOutputValidator,
    FinishTestResultValidator,
)
from cato_server.domain.image import ImageChannel
from cato_server.domain.output import Output
from cato_server.domain.test_identifier import TestIdentifier
from cato_server.domain.test_result import TestResult
from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.mappers.page_mapper import PageMapper
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.output_repository import OutputRepository
from cato_server.storage.abstract.page import PageRequest
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)
from cato_server.usecases.finish_test import FinishTest

logger = logging.getLogger(__name__)


class TestResultsBlueprint(BaseBlueprint):
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        suite_result_repository: SuiteResultRepository,
        file_storage: AbstractFileStorage,
        output_repository: OutputRepository,
        image_repository: ImageRepository,
        finish_test: FinishTest,
        object_mapper: ObjectMapper,
        page_mapper: PageMapper,
    ):
        super(TestResultsBlueprint, self).__init__("test-results", __name__)
        self._test_result_repository = test_result_repository
        self._suite_result_repository = suite_result_repository
        self._file_storage = file_storage
        self._output_repository = output_repository
        self._image_repository = image_repository
        self._finish_test = finish_test
        self._object_mapper = object_mapper
        self._page_mapper = page_mapper

        self.route(
            "/test_results/suite_result/<int:suite_result_id>/<string:suite_name>/<string:test_name>",
            methods=["GET"],
        )(self.get_test_result_by_suite_and_identifier)
        self.route(
            "/test_results/runs/<int:run_id>/<string:suite_name>/<string:test_name>",
            methods=["GET"],
        )(self.get_test_result_by_run_id_and_identifier)
        self.route("/test_results/suite_result/<int:suite_id>", methods=["GET"])(
            self.get_test_result_by_suite_id
        )
        self.route("/test_results/<int:test_result_id>/output", methods=["GET"])(
            self.get_test_result_output
        )
        self.route("/test_results/output", methods=["POST"])(
            self.create_test_result_output
        )
        self.route("/test_results", methods=["POST"])(self.create_test_result)
        self.route("/test_results/<int:test_result_id>", methods=["PATCH"])(
            self.update_test_result
        )
        self.route("/test_results/run/<int:run_id>", methods=["GET"])(
            self.get_test_result_by_run_id
        )

        self.route(
            "/test_results/run/<int:run_id>/test_status/<test_status>", methods=["GET"]
        )(self.get_test_result_by_run_id_and_test_status)

        self.route("/test_results/<int:test_result_id>", methods=["GET"])(
            self.get_test_result_by_id
        )
        self.route("/test_results/finish", methods=["POST"])(self.finish_test_result)

    def get_test_result_by_suite_and_identifier(
        self, suite_result_id, suite_name, test_name
    ):
        identifier = TestIdentifier(suite_name, test_name)
        test_result = (
            self._test_result_repository.find_by_suite_result_and_test_identifier(
                suite_result_id, identifier
            )
        )
        if not test_result:
            abort(404)

        return self.json_response(self._object_mapper.to_json(test_result)), 200

    def get_test_result_by_run_id_and_identifier(self, run_id, suite_name, test_name):
        identifier = TestIdentifier(suite_name, test_name)
        suite_result = self._suite_result_repository.find_by_run_id_and_name(
            run_id, suite_name
        )
        if not suite_result:
            abort(404)

        test_result = (
            self._test_result_repository.find_by_suite_result_and_test_identifier(
                suite_result.id, identifier
            )
        )
        if not test_result:
            abort(404)

        return self.json_response(self._object_mapper.to_json(test_result))

    def get_test_result_by_suite_id(self, suite_id):
        test_results = self._test_result_repository.find_by_suite_result_id(suite_id)
        return self.json_response(self._object_mapper.many_to_json(test_results))

    def get_test_result_output(self, test_result_id):
        output = self._output_repository.find_by_test_result_id(test_result_id)
        if not output:
            abort(404)
        return self.json_response(self._object_mapper.to_json(output))

    def create_test_result(self):
        request_json = request.get_json()
        errors = CreateTestResultValidator(
            self._suite_result_repository, self._file_storage
        ).validate(request_json)
        if errors:
            return jsonify(errors), BAD_REQUEST

        test_result = self._object_mapper.from_dict(request_json, TestResult)

        test_result = self._test_result_repository.save(test_result)
        logger.info("Created TestResult %s", test_result)
        return self.json_response(self._object_mapper.to_json(test_result)), 201

    def update_test_result(self, test_result_id):
        request_json = request.get_json()
        errors = UpdateTestResultValidator(
            self._suite_result_repository, self._file_storage
        ).validate(request_json)
        if errors:
            return jsonify(errors), BAD_REQUEST

        test_result = self._test_result_repository.find_by_id(test_result_id)
        if not test_result:
            abort(404)

        update_data_keys = UpdateTestResultSchema().load(request_json).keys()
        update_data = {key: request_json[key] for key in update_data_keys}

        test_result_dict = self._object_mapper.to_dict(test_result)
        logger.info("Updating TestResult with data %s", update_data)
        test_result_dict.update(update_data)
        test_result = self._object_mapper.from_dict(test_result_dict, TestResult)

        logger.info("Saving updated TestResult %s", test_result)
        self._test_result_repository.save(test_result)
        return jsonify(test_result_dict), 200

    def create_test_result_output(self):
        request_json = request.get_json()
        errors = CreateOutputValidator(
            self._test_result_repository, self._output_repository
        ).validate(request_json)
        if errors:
            return jsonify(errors), BAD_REQUEST

        output = self._object_mapper.from_dict(request_json, Output)
        logger.info(
            "Saving output for test result with id %s", request_json["test_result_id"]
        )
        output = self._output_repository.save(output)
        return self.json_response(self._object_mapper.to_json(output)), 201

    def get_test_result_by_run_id(self, run_id: int):
        page_request = page_request_from_request(request.args)
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
        return self.json_response(
            self._object_mapper.many_to_json(test_result_short_summary_dtos)
        )

    def _get_test_result_by_run_id_paged(self, run_id: int, page_request: PageRequest):
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
        return self.json_response(self._page_mapper.to_json(page))

    def get_test_result_by_id(self, test_result_id):
        result = self._test_result_repository.find_by_id(test_result_id)
        if not result:
            abort(404)

        image_output_dto = None
        reference_image_dto = None

        image_output = self._image_repository.find_by_id(result.image_output)
        if result.image_output and image_output:
            image_output_dto = ImageDto(
                id=image_output.id,
                name=image_output.name,
                original_file_id=image_output.original_file_id,
                channels=list(map(self._to_channel_dto, image_output.channels)),
                width=image_output.width,
                height=image_output.height,
            )

        reference_image = self._image_repository.find_by_id(result.reference_image)
        if result.reference_image and reference_image:
            reference_image_dto = ImageDto(
                id=reference_image.id,
                name=reference_image.name,
                original_file_id=reference_image.original_file_id,
                channels=list(map(self._to_channel_dto, reference_image.channels)),
                width=reference_image.width,
                height=reference_image.height,
            )

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
            ),
            execution_status=ExecutionStatusDto(result.execution_status.value),
            status=TestStatusDto(result.status.value) if result.status else None,
            seconds=result.seconds if result.seconds is not None else 0,
            message=result.message if result.message else None,
            image_output=image_output_dto,
            reference_image=reference_image_dto,
            started_at=result.started_at.isoformat() if result.started_at else None,
            finished_at=result.finished_at.isoformat() if result.finished_at else None,
        )
        return self.json_response(self._object_mapper.to_json(test_result_dto))

    def _to_channel_dto(self, channel: ImageChannel):
        return ImageChannelDto(
            id=channel.id, name=channel.name, file_id=channel.file_id
        )

    def finish_test_result(self):
        request_json = request.get_json()
        errors = FinishTestResultValidator(
            self._test_result_repository, self._image_repository
        ).validate(request_json)
        if errors:
            return jsonify(errors), BAD_REQUEST

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
        )

        return jsonify(success=True), 200

    def get_test_result_by_run_id_and_test_status(self, run_id, test_status):
        try:
            test_status = TestStatus(test_status)
        except ValueError:
            return (
                jsonify({"test_status": f"Not a valid test status: {test_status}."}),
                400,
            )
        test_results = (
            self._test_result_repository.find_by_run_id_filter_by_test_status(
                run_id, test_status
            )
        )

        test_identifiers = list(map(lambda x: x.test_identifier, test_results))

        return (
            self.json_response(self._object_mapper.many_to_json(test_identifiers)),
            200,
        )
