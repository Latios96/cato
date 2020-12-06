import dataclasses
import logging
from http.client import BAD_REQUEST

from flask import Blueprint, jsonify, abort, request

from cato.domain.test_identifier import TestIdentifier
from cato.mappers.test_result_class_mapper import TestResultClassMapper
from cato.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato.storage.abstract.abstract_test_result_repository import TestResultRepository
from cato.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.api.validators.test_result_validators import CreateTestResultValidator

logger = logging.getLogger(__name__)


class TestResultsBlueprint(Blueprint):
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        suite_result_repository: SuiteResultRepository,
        file_storage: AbstractFileStorage,
    ):
        super(TestResultsBlueprint, self).__init__("test-results", __name__)
        self._test_result_repository = test_result_repository
        self._suite_result_repository = suite_result_repository
        self._file_storage = file_storage

        self._test_result_mapper = TestResultClassMapper()

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
        self.route("/test_results", methods=["POST"])(self.create_test_result)

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
        test_result = dataclasses.asdict(test_result)
        test_result.pop("output")
        return jsonify(test_result)

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

        test_result = dataclasses.asdict(test_result)
        test_result.pop("output")
        return jsonify(test_result)

    def get_test_result_by_suite_id(self, suite_id):
        test_results = self._test_result_repository.find_by_suite_result(suite_id)
        mapped_results = []
        for result in test_results:
            result = dataclasses.asdict(result)
            result.pop("output")
            mapped_results.append(result)
        return jsonify(mapped_results)

    def get_test_result_output(self, test_result_id):
        suite_result = self._test_result_repository.find_by_id(test_result_id)
        if not suite_result:
            abort(404)
        return jsonify(suite_result.output)

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
        return jsonify(self._test_result_mapper.map_to_dict(test_result)), 201
