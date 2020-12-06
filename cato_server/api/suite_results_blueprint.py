import logging
from http.client import BAD_REQUEST

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.domain.suite_result import SuiteResult
from cato_server.api.validators.suite_result_validators import (
    CreateSuiteResultValidator,
)

logger = logging.getLogger(__name__)


def run_id_exists(self, id):
    return self._run_repository.find_by_id(id) is not None


class SuiteResultsBlueprint(Blueprint):
    def __init__(
        self,
        suite_result_repository: SuiteResultRepository,
        run_repository: RunRepository,
    ):
        super(SuiteResultsBlueprint, self).__init__("suite-results", __name__)
        self._suite_result_repository = suite_result_repository
        self._run_repository = run_repository

        self.route("/suite_results/run/<run_id>", methods=["GET"])(
            self.suite_result_by_run
        )
        self.route("/suite_results", methods=["POST"])(self.create_suite_result)

    def suite_result_by_run(self, run_id):
        suite_results = self._suite_result_repository.find_by_run_id(run_id)
        return jsonify(suite_results)

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
        return jsonify(suite_result), 201

    def _run_id_exists(self, id):
        if self._run_repository.find_by_id(id) is None:
            raise ValidationError(f"No run with id {id} exists.")

    def _is_str_str_dict(self, the_dict):
        for key, value in the_dict.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise ValidationError(f"Not a mapping of str->str: {key}={value}")
