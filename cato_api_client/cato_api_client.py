import logging
import os
from typing import Optional, Type, TypeVar, Iterable
from urllib.parse import quote

import requests

import cato_api_client.api_client_logging  # noqa: F401
from cato.domain.test_status import TestStatus
from cato_api_client.http_template import AbstractHttpTemplate
from cato_api_models.catoapimodels import (
    CreateFullRunDto,
    FinishTestResultDto,
    TestStatusDto,
    TestHeartbeatDto,
    ApiSuccess,
    StartTestResultDto,
)
from cato_server.domain.file import File
from cato_server.domain.image import Image
from cato_server.domain.output import Output
from cato_server.domain.project import Project
from cato_server.domain.run import Run
from cato_server.domain.suite_result import SuiteResult
from cato_server.domain.test_identifier import TestIdentifier
from cato_server.domain.test_result import TestResult
from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.domain.submission_info import SubmissionInfo

logger = logging.getLogger(__name__)

T = TypeVar("T")
R = TypeVar("R")


class CatoApiClient:
    def __init__(
        self, url: str, http_template: AbstractHttpTemplate, object_mapper: ObjectMapper
    ) -> None:
        self._url = url
        self._http_template = http_template
        self._object_mapper = object_mapper

    def get_project_by_name(self, project_name: str) -> Optional[Project]:
        url = self._build_url("/api/v1/projects/name/{}".format(project_name))
        return self._find_with_http_template(url, Project)

    def create_project(self, project_name: str) -> Project:
        url = self._build_url("/api/v1/projects")
        logger.info("Creating project with name %s..", project_name)
        return self._create_with_http_template(url, {"name": project_name}, Project)

    def upload_file(self, path: str) -> File:
        if not os.path.exists(path):
            raise ValueError(f"Path {path} does not exists!")

        url = self._build_url("/api/v1/files")
        files = {"file": open(path, "rb")}

        logger.info("Uploading file %s", path)
        response = self._post_form(url, {}, files=files)

        if response.status_code == 201:
            return self._object_mapper.from_dict(self._get_json(response), File)
        raise self._create_value_error_for_bad_request(response)

    def upload_image(self, path: str) -> Image:
        if not os.path.exists(path):
            raise ValueError(f"Path {path} does not exists!")

        url = self._build_url("/api/v1/images")
        files = {"file": open(path, "rb")}

        logger.info("Uploading image %s", path)
        response = self._post_form(url, {}, files=files)

        if response.status_code == 201:
            return self._object_mapper.from_dict(self._get_json(response), Image)
        raise self._create_value_error_for_bad_request(response)

    def create_suite_result(self, suite_result: SuiteResult) -> SuiteResult:
        if suite_result.id:
            raise ValueError(f"Id of SuiteResult is not 0, was {suite_result.id}")

        url = self._build_url("/api/v1/suite_results")
        logger.info("Creating suite_result with data %s..", suite_result)
        return self._create_with_http_template(url, suite_result, SuiteResult)

    def create_run(self, run: Run) -> Run:
        if run.id:
            raise ValueError(f"Id of Run is not 0, was {run.id}")

        url = self._build_url("/api/v1/runs")
        logger.info("Creating run with data %s..", run)
        return self._create_with_http_template(url, run, Run)

    def create_full_run(self, create_full_run_dto: CreateFullRunDto) -> Run:
        url = self._build_url("/api/v1/runs/full")
        return self._create_with_http_template(url, create_full_run_dto, Run)

    def create_test_result(self, test_result: TestResult) -> TestResult:
        if test_result.id:
            raise ValueError(f"Id of TestResult is not 0, was {test_result.id}")

        url = self._build_url("/api/v1/test_results")
        logger.info("Creating test_result with data %s..", test_result)
        return self._create_with_http_template(url, test_result, TestResult)

    def find_test_result_by_run_id_and_identifier(
        self, run_id: int, test_identifier: TestIdentifier
    ) -> Optional[TestResult]:
        url = self._build_url(
            "/api/v1/test_results/runs/{}/{}/{}".format(
                run_id, test_identifier.suite_name, test_identifier.test_name
            )
        )
        return self._find_with_http_template(url, TestResult)

    def run_id_exists(self, run_id: int) -> bool:
        url = self._build_url(
            "/api/v1/runs/{}/exists".format(run_id)
        )  # todo use ApiSuccess class
        response = self._get_url(url)
        if response.status_code == 200:
            return True
        elif response.status_code == 404:
            return False
        raise ValueError(f"Something went wrong: {response}")

    def upload_output(self, test_result_id: int, output: str) -> Output:
        url = self._build_url("/api/v1/test_results/output")
        return self._create_with_http_template(
            url, {"test_result_id": test_result_id, "text": output}, Output
        )

    def heartbeat_test(self, run_id: int, test_identifier: TestIdentifier) -> None:
        url = self._build_url(
            f"/api/v1/test_heartbeats/run/{run_id}/{test_identifier.suite_name}/{test_identifier.test_name}"
        )
        response = self._http_template.post_for_entity(url, {}, TestHeartbeatDto)
        if response.status_code() != 200:
            raise ValueError(f"Something went wrong when sending heartbeat: {response}")

    def start_test(self, test_result_id: int) -> None:
        url = self._build_url("/api/v1/test_results/start")
        dto = StartTestResultDto(
            id=test_result_id,
        )
        response = self._http_template.post_for_entity(url, dto, StartTestResultDto)
        if response.status_code() != 200:
            raise ValueError(
                f"Something went wrong when starting test: {response.status_code()}, {response.text()}"
            )

    def finish_test(
        self,
        test_result_id: int,
        status: TestStatus,
        seconds: float,
        message: str,
        image_output: Optional[int] = None,
        reference_image: Optional[int] = None,
    ) -> None:
        url = self._build_url("/api/v1/test_results/finish")
        dto = FinishTestResultDto(
            id=test_result_id,
            status=TestStatusDto(status.value),
            seconds=seconds,
            message=message,
            image_output=image_output,
            reference_image=reference_image,
        )
        response = self._http_template.post_for_entity(url, dto, FinishTestResultDto)
        if response.status_code() != 200:
            raise ValueError(
                f"Something went wrong when finishing test: {response.status_code()}, {response.text()}"
            )

    def generate_run_url(self, project_id: int, run_id: int) -> str:
        return f"{self._url}/#/projects/{project_id}/runs/{run_id}"

    def get_test_results_by_run_id_and_test_status(
        self, run_id: int, test_status: TestStatus
    ) -> Optional[Iterable[TestIdentifier]]:
        url = self._build_url(
            f"/api/v1/test_results/run/{run_id}/test_status/{test_status.value}"
        )

        return self._find_many_with_http_template(url, TestIdentifier)

    def submit_to_scheduler(self, submission_info: SubmissionInfo) -> None:
        url = self._build_url("/api/v1/schedulers/submit")
        response = self._http_template.post_for_entity(url, submission_info, ApiSuccess)
        if response.status_code() != 200 or not response.get_entity().success:
            raise ValueError(
                f"Something went wrong when submitting to scheduler: {response.status_code()}, {response.text()}"
            )

    def get_submission_info_by_id(
        self, submission_info_id: int
    ) -> Optional[SubmissionInfo]:
        url = self._build_url("/api/v1/submission_infos/{}".format(submission_info_id))
        return self._find_with_http_template(url, SubmissionInfo)

    def _build_url(self, url):
        return self._url + quote(url)

    def _get_json(self, reponse):
        return reponse.json()

    def _create_with_http_template(self, url: str, body: T, response_cls: Type[R]) -> R:
        response = self._http_template.post_for_entity(url, body, response_cls)
        if response.status_code() == 201:
            return response.get_entity()
        raise ValueError(
            "Bad parameters: {}".format(
                " ".join(
                    [
                        "{}: {}".format(key, value)
                        for key, value in response.get_json().items()
                    ]
                )
            )
        )

    def _patch_with_http_template(self, url, body, response_cls):
        response = self._http_template.patch_for_entity(url, body, response_cls)
        if response.status_code() == 200:
            return response.get_entity()
        raise ValueError(
            "Bad parameters: {}".format(
                " ".join(
                    [
                        "{}: {}".format(key, value)
                        for key, value in response.get_json().items()
                    ]
                )
            )
        )

    def _create_value_error_for_bad_request(self, response):
        return ValueError(
            "Bad parameters: {}".format(
                " ".join(
                    [
                        "{}: {}".format(key, value)
                        for key, value in self._get_json(response).items()
                    ]
                )
            )
        )

    def _post_form(self, url, params, files=None):
        logger.debug("Launching POST request to %s with params %s", url, params)
        response = requests.post(url, data=params, files=files)
        logger.debug("Received response %s", response)
        return response

    def _find_with_http_template(self, url: str, response_cls: Type[T]) -> Optional[T]:
        response = self._http_template.get_for_entity(url, response_cls)
        if response.status_code() == 404:
            return None
        if response.status_code() == 200:
            return response.get_entity()
        raise ValueError(
            "Bad parameters: {}".format(
                " ".join(
                    [
                        "{}: {}".format(key, value)
                        for key, value in response.get_json().items()
                    ]
                )
            )
        )

    def _find_many_with_http_template(
        self, url: str, response_cls: Type[T]
    ) -> Optional[Iterable[T]]:
        response = self._http_template.get_for_entity(url, response_cls)
        if response.status_code() == 404:
            return None
        if response.status_code() == 200:
            return response.get_entities()
        raise ValueError(
            "Bad parameters: {}".format(
                " ".join(
                    [
                        "{}: {}".format(key, value)
                        for key, value in response.get_json().items()
                    ]
                )
            )
        )

    def _get_url(self, url):
        logger.debug("Launching GET request to %s", url)
        response = requests.get(url)
        logger.debug("Received response %s", response)
        return response
