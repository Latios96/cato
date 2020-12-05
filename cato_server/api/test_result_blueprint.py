import dataclasses
import logging

from flask import Blueprint, jsonify, abort
from marshmallow import Schema, fields
from marshmallow.validate import Length, Regexp
from marshmallow_enum import EnumField

from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_result import TestStatus
from cato.storage.abstract.abstract_test_result_repository import TestResultRepository
from cato.storage.domain.execution_status import ExecutionStatus

logger = logging.getLogger(__name__)


class TestResultsBlueprint(Blueprint):
    def __init__(self, test_result_repository: TestResultRepository):
        super(TestResultsBlueprint, self).__init__("test-results", __name__)
        self._test_result_repository = test_result_repository

        self.route(
            "/test_results/suite_result/<int:suite_result_id>/<string:suite_name>/<string:test_name>",
            methods=["GET"],
        )(self.get_test_result_by_suite_and_identifier)
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
        suite_result = (
            self._test_result_repository.find_by_suite_result_and_test_identifier(
                suite_result_id, identifier
            )
        )
        if not suite_result:
            abort(404)
        suite_result = dataclasses.asdict(suite_result)
        suite_result.pop("output")
        return jsonify(suite_result)

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
        class MachineInfoSchema(Schema):
            cpu_name: fields.String(required=True, validate=[Length(1)])
            cores: fields.Integer(required=True, min=1)
            memory: fields.Float(required=True, min=0)

        class CreateTestResultSchema(Schema):
            suite_result_id: fields.Integer(required=True)
            test_name: fields.String(
                required=True, validate=[Length(min=1), Regexp(r"^[A-Za-z0-9_\-]+$")]
            )
            test_identifier: fields.String(
                required=True, validate=[Length(min=1), self._is_test_identifier]
            )
            test_command: fields.String(required=True, validate=[Length(1)])
            test_variables: fields.Dict(required=True)
            machine_info: fields.Nested(MachineInfoSchema, required=True)
            execution_status: EnumField(ExecutionStatus, required=True)
            status = EnumField(TestStatus)
            output = fields.List(fields.String())
            seconds = fields.Float(min=1)
            message = fields.String(validate=[Length(1)])
            image_output = fields.Integer()
            reference_image = fields.Integer()
            started_at = fields.DateTime()
            finished_at = fields.DateTime()

    def _is_test_identifier(self, test_identifier):
        raise NotImplementedError()
