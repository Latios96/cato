import logging
from http.client import BAD_REQUEST

from flask import Blueprint, jsonify, request, abort
from marshmallow import ValidationError

from cato_server.api.base_blueprint import BaseBlueprint
from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.mappers.suite_result_dto_mapper import SuiteResultDtoDtoClassMapper
from cato_server.mappers.suite_result_summary_dto_mapper import (
    SuiteResultSummaryDtoClassMapper,
)
from cato_server.run_status_calculator import RunStatusCalculator
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.domain.suite_result import SuiteResult
from cato_server.api.validators.suite_result_validators import (
    CreateSuiteResultValidator,
)
from cato_api_models.catoapimodels import (
    SuiteResultDto,
    SuiteStatusDto,
    SuiteResultSummaryDto,
    TestResultShortSummaryDto,
    ExecutionStatusDto,
    TestStatusDto,
)

logger = logging.getLogger(__name__)


def run_id_exists(self, id):
    return self._run_repository.find_by_id(id) is not None


class SuiteResultsBlueprint(BaseBlueprint):
    def __init__(
        self,
        suite_result_repository: SuiteResultRepository,
        run_repository: RunRepository,
        test_result_repository: TestResultRepository,
        object_mapper: ObjectMapper,
    ):
        super(SuiteResultsBlueprint, self).__init__("suite-results", __name__)
        self._suite_result_repository = suite_result_repository
        self._run_repository = run_repository
        self._test_result_repository = test_result_repository
        self._object_mapper = object_mapper

        self._status_calculator = RunStatusCalculator()

        self.route("/suite_results/run/<run_id>", methods=["GET"])(
            self.suite_result_by_run
        )
        self.route("/suite_results/<suite_id>", methods=["GET"])(
            self.suite_result_by_id
        )
        self.route("/suite_results", methods=["POST"])(self.create_suite_result)

    def suite_result_by_run(self, run_id):
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
        return self.json_response(self._object_mapper.many_to_json(suite_result_dtos))

    def create_suite_result(self):
        request_json = request.get_json()
        errors = CreateSuiteResultValidator(
            self._run_repository, self._suite_result_repository
        ).validate(request_json)
        if errors:
            return jsonify(errors), BAD_REQUEST

        suite_result = SuiteResult(
            id=0,
            run_id=request_json["run_id"],
            suite_name=request_json["suite_name"],
            suite_variables=request_json["suite_variables"],
        )
        suite_result = self._suite_result_repository.save(suite_result)
        logger.info("Created SuiteResult %s", suite_result)
        return self.json_response(self._object_mapper.to_json(suite_result)), 201

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
            abort(404)

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
        return self.json_response(self._object_mapper.to_json(dto))
