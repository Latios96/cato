import logging
from http.client import BAD_REQUEST
from typing import Iterable

from flask import Blueprint, jsonify, abort, request

from cato_server.domain.test_identifier import TestIdentifier
from cato_server.domain.test_result import TestResult
from cato_server.mappers.output_class_mapper import OutputClassMapper
from cato_server.mappers.test_result_class_mapper import TestResultClassMapper
from cato_server.api.schemas.test_result_schemas import UpdateTestResultSchema
from cato_server.api.validators.test_result_validators import (
    CreateTestResultValidator,
    UpdateTestResultValidator,
    CreateOutputValidator,
)
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.abstract_test_result_repository import (
    TestResultRepository,
)
from cato_server.storage.abstract.output_repository import OutputRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository

logger = logging.getLogger(__name__)


class TestResultsBlueprint(Blueprint):
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        suite_result_repository: SuiteResultRepository,
        file_storage: AbstractFileStorage,
        output_repository: OutputRepository,
    ):
        super(TestResultsBlueprint, self).__init__("test-results", __name__)
        self._test_result_repository = test_result_repository
        self._suite_result_repository = suite_result_repository
        self._file_storage = file_storage
        self._output_repository = output_repository

        self._test_result_mapper = TestResultClassMapper()
        self._output_class_mapper = OutputClassMapper()

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

        self.route("/test_results/<int:test_result_id>", methods=["GET"])(
            self.get_test_result_by_id
        )

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
        return self._map_test_result(test_result)

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

        return self._map_test_result(test_result)

    def get_test_result_by_suite_id(self, suite_id):
        test_results = self._test_result_repository.find_by_suite_result(suite_id)
        return self._map_many_test_results(test_results)

    def get_test_result_output(self, test_result_id):
        output = self._output_repository.find_by_test_result_id(test_result_id)
        if not output:
            abort(404)
        return jsonify(output)

    def create_test_result(self):
        request_json = request.get_json()
        errors = CreateTestResultValidator(
            self._suite_result_repository, self._file_storage
        ).validate(request_json)
        if errors:
            return jsonify(errors), BAD_REQUEST

        test_result = self._test_result_mapper.map_from_dict(request_json)

        test_result = self._test_result_repository.save(test_result)
        logger.info("Created TestResult %s", test_result)
        return self._map_test_result(test_result, 201)

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

        test_result_dict = self._test_result_mapper.map_to_dict(test_result)
        logger.info("Updating TestResult with data %s", update_data)
        test_result_dict.update(update_data)
        test_result = self._test_result_mapper.map_from_dict(test_result_dict)

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

        output = self._output_class_mapper.map_from_dict(request_json)
        logger.info(
            "Saving output for test result with id %s", request_json["test_result_id"]
        )
        output = self._output_repository.save(output)
        return jsonify(self._output_class_mapper.map_to_dict(output)), 201

    def _map_test_result(self, test_result: TestResult, status=200):
        test_result = self._test_result_mapper.map_to_dict(test_result)
        return jsonify(test_result), status

    def _map_many_test_results(self, test_results: Iterable[TestResult]):
        mapped_results = []
        for result in test_results:
            result = self._test_result_mapper.map_to_dict(result)
            mapped_results.append(result)
        return jsonify(mapped_results)

    def get_test_result_by_run_id(self, run_id: int):
        test_results = self._test_result_repository.find_by_run_id(run_id)
        return jsonify(self._test_result_mapper.map_many_to_dict(test_results))

    def get_test_result_by_id(self, test_result_id):
        result = self._test_result_repository.find_by_id(test_result_id)
        if not result:
            abort(404)
        return jsonify(self._test_result_mapper.map_to_dict(result))
