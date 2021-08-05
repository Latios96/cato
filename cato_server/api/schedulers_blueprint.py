import logging
from http.client import BAD_REQUEST

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from cato.config.config_file_parser import JsonConfigParser
from cato_server.api.validators.test_submission_validators import (
    SubmissionInfoValidator,
)
from cato_server.configuration.optional_component import OptionalComponent
from cato_server.schedulers.abstract_scheduler_submitter import (
    AbstractSchedulerSubmitter,
)
from cato_common.domain.submission_info import SubmissionInfo
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.submission_info_repository import (
    SubmissionInfoRepository,
)

logger = logging.getLogger(__name__)


class SchedulersBlueprint(APIRouter):
    def __init__(
        self,
        run_repository: RunRepository,
        scheduler_submitter: OptionalComponent[AbstractSchedulerSubmitter],
        json_config_parser: JsonConfigParser,
        submission_info_repository: SubmissionInfoRepository,
    ):
        super(SchedulersBlueprint, self).__init__()
        self._run_repository = run_repository
        self._scheduler_submitter = scheduler_submitter
        self._json_config_parser = json_config_parser
        self._submission_info_repository = submission_info_repository

        if self._scheduler_submitter.is_available():
            self.post("/schedulers/submit")(self.submit_tests)
        else:
            self.post("/schedulers/submit")(self.submit_tests_placeholder)

    async def submit_tests(self, request: Request) -> Response:
        request_json = await request.json()
        errors = SubmissionInfoValidator(self._run_repository).validate(request_json)
        if errors:
            return JSONResponse(content=errors, status_code=BAD_REQUEST)

        submission_info = self._read_submission_info(request_json)
        submission_info = self._submission_info_repository.save(submission_info)

        self._scheduler_submitter.component.submit_tests(submission_info)

        return JSONResponse(content={"success": True})

    def _read_submission_info(self, request_json) -> SubmissionInfo:
        return SubmissionInfo(
            id=0,
            config=self._json_config_parser.parse_dict(request_json["config"]),
            run_id=request_json["run_id"],
            resource_path=request_json["resource_path"],
            executable=request_json["executable"],
        )

    def submit_tests_placeholder(self) -> Response:
        return JSONResponse(
            content={"message": "No scheduler is available!"}, status_code=404
        )
