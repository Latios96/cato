import logging
from http.client import BAD_REQUEST

from flask import Blueprint, request, jsonify

from cato.config.config_file_parser import JsonConfigParser
from cato_server.api.validators.test_submission_validators import (
    SubmissionInfoValidator,
)
from cato_server.configuration.optional_component import OptionalComponent
from cato_server.schedulers.abstract_scheduler_submitter import (
    AbstractSchedulerSubmitter,
)
from cato_server.domain.submission_info import SubmissionInfo
from cato_server.storage.abstract.run_repository import RunRepository

logger = logging.getLogger(__name__)


class SchedulersBlueprint(Blueprint):
    def __init__(
        self,
        run_repository: RunRepository,
        scheduler_submitter: OptionalComponent[AbstractSchedulerSubmitter],
        json_config_parser: JsonConfigParser,
    ):
        super(SchedulersBlueprint, self).__init__("schedulers", __name__)
        self._run_repository = run_repository
        self._scheduler_submitter = scheduler_submitter
        self._json_config_parser = json_config_parser

        if self._scheduler_submitter.is_available():
            self.route("/schedulers/submit", methods=["POST"])(self.submit_tests)
        else:
            self.route("/schedulers/submit", methods=["POST"])(
                self.submit_tests_placeholder
            )

    def submit_tests(self):
        request_json = request.get_json()
        errors = SubmissionInfoValidator(self._run_repository).validate(request_json)
        if errors:
            return jsonify(errors), BAD_REQUEST

        submission_info = self._read_submission_info(request_json)

        self._scheduler_submitter.component.submit_tests(submission_info)

        return jsonify(success=True), 200

    def _read_submission_info(self, request_json):
        return SubmissionInfo(
            id=0,
            config=self._json_config_parser.parse_dict(request_json["config"]),
            run_id=request_json["run_id"],
            resource_path=request_json["resource_path"],
            executable=request_json["executable"],
        )

    def submit_tests_placeholder(self):
        return jsonify(message="No scheduler is available!"), 404
