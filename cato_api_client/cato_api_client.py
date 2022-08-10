import datetime
import logging
import os
from typing import Optional, Type, TypeVar, List, Dict, Callable
from urllib.parse import quote

import cato_api_client.api_client_logging  # noqa: F401
from cato.domain.comparison_settings import ComparisonSettings
from cato_api_client.http_template import HttpTemplate
from cato_api_client.task_result_template import TaskResultTemplate
from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_common.domain.compare_image_result import CompareImageResult
from cato_common.domain.file import File
from cato_common.domain.image import Image
from cato_common.domain.output import Output
from cato_common.domain.project import Project
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.run import Run
from cato_common.domain.submission_info import SubmissionInfo
from cato_common.domain.tasks.task_result import TaskResult
from cato_common.domain.test_edit import (
    AbstractTestEdit,
    ComparisonSettingsEdit,
    ReferenceImageEdit,
)
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.test_result import TestResult
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.dtos.create_full_run_dto import CreateFullRunDto
from cato_common.dtos.finish_test_result_dto import FinishTestResultDto
from cato_common.dtos.start_test_result_dto import StartTestResultDto
from cato_common.dtos.store_image_result import StoreImageResult
from cato_common.dtos.upload_output_dto import UploadOutputDto
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.api.dtos.api_success import ApiSuccess
from cato_server.domain.test_heartbeat import TestHeartbeat

logger = logging.getLogger(__name__)
T = TypeVar("T")
R = TypeVar("R")


class CatoApiClient:
    def __init__(
        self,
        url: str,
        http_template: HttpTemplate,
        object_mapper: ObjectMapper,
        api_token_provider: Callable[[], ApiTokenStr],
    ) -> None:
        self._url = url
        self._http_template = http_template
        self._object_mapper = object_mapper
        if api_token_provider:
            self._login(api_token_provider())
        self._task_result_template = TaskResultTemplate(
            self._http_template, self._object_mapper
        )

    def _login(self, api_token_str: ApiTokenStr):
        self._http_template.set_authorization_header(str(api_token_str.to_bearer()))
        self._http_template.get_for_entity(
            self._build_url("/api_tokens/is_valid"), ApiSuccess
        )

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
        response = self._http_template.post_files_for_entity(url, None, files, File)

        if response.status_code() == 201:
            return response.get_entity()
        raise self._create_value_error_for_bad_request(response)

    def upload_image(self, path: str) -> Image:
        if not os.path.exists(path):
            raise ValueError(f"Path {path} does not exists!")

        url = self._build_url("/api/v1/images")
        files = {"file": (os.path.basename(path), open(path, "rb"))}

        logger.info("Uploading image %s", path)
        response = self._http_template.post_files_for_entity(
            url, None, files, TaskResult
        )

        if response.status_code() == 201:
            task_result = response.get_entity()
            store_image_result = (
                self._task_result_template.wait_for_task_result_to_complete(
                    task_result,
                    StoreImageResult,
                    timeout=datetime.timedelta(seconds=120),
                    poll_interval=datetime.timedelta(seconds=1),
                )
            )
            return store_image_result.image

    def download_original_image(self, image_id: int) -> Optional[bytes]:
        url = self._build_url(f"/api/v1/images/original_file/{image_id}")
        response = self._http_template.get_for_entity(url, object)
        if response.status_code() == 404:
            return None
        if response.status_code() != 200:
            raise ValueError(
                f"Something went wrong when downloading original image: {response}"
            )
        return response.content()

    def get_image_by_id(self, image_id: int) -> Optional[Image]:
        url = self._build_url(f"/api/v1/images/{image_id}")
        return self._find_with_http_template(url, Image)

    def compare_images(
        self,
        reference_image: str,
        output_image: str,
        comparison_settings: ComparisonSettings,
    ) -> CompareImageResult:
        if not os.path.exists(reference_image):
            raise ValueError(f"Path {reference_image} does not exists!")

        if not os.path.exists(output_image):
            raise ValueError(f"Path {output_image} does not exists!")

        url = self._build_url("/api/v1/compare_image")
        files = {
            "reference_image": (
                os.path.basename(reference_image),
                open(reference_image, "rb"),
            ),
            "output_image": (
                os.path.basename(output_image),
                open(output_image, "rb"),
            ),
        }

        data = {"comparison_settings": self._object_mapper.to_json(comparison_settings)}

        logger.info("Uploading images for comparison..")
        logger.info(
            "Uploading reference image %s, output image %s with comparison settings %s",
            reference_image,
            output_image,
            comparison_settings,
        )
        response = self._http_template.post_files_for_entity(
            url, data, files, CompareImageResult
        )

        if response.status_code() == 201:
            return response.get_entity()
        raise self._create_value_error_for_bad_request(response)

    def compare_images_async(
        self,
        reference_image: str,
        output_image: str,
        comparison_settings: ComparisonSettings,
    ) -> CompareImageResult:
        if not os.path.exists(reference_image):
            raise ValueError(f"Path {reference_image} does not exists!")

        if not os.path.exists(output_image):
            raise ValueError(f"Path {output_image} does not exists!")

        url = self._build_url("/api/v1/compare_image-async")
        files = {
            "reference_image": (
                os.path.basename(reference_image),
                open(reference_image, "rb"),
            ),
            "output_image": (
                os.path.basename(output_image),
                open(output_image, "rb"),
            ),
        }

        data = {"comparison_settings": self._object_mapper.to_json(comparison_settings)}

        logger.info("Uploading images for comparison..")
        logger.info(
            "Uploading reference image %s, output image %s with comparison settings %s",
            reference_image,
            output_image,
            comparison_settings,
        )
        response = self._http_template.post_files_for_entity(
            url, data, files, TaskResult
        )

        if response.status_code() == 201:
            task_result = response.get_entity()
            compare_image_result = (
                self._task_result_template.wait_for_task_result_to_complete(
                    task_result,
                    CompareImageResult,
                    timeout=datetime.timedelta(seconds=120),
                    poll_interval=datetime.timedelta(seconds=1),
                )
            )
            return compare_image_result
        raise self._create_value_error_for_bad_request(response)

    def create_run(self, create_run_dto: CreateFullRunDto) -> Run:
        url = self._build_url("/api/v1/runs/full")
        return self._create_with_http_template(url, create_run_dto, Run)

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
        url = self._build_url("/api/v1/runs/{}/exists".format(run_id))
        response = self._http_template.get_for_entity(url, ApiSuccess)
        if response.status_code() == 200:
            return True
        elif response.status_code() == 404:
            return False
        raise ValueError(f"Something went wrong: {response}")

    def upload_output(self, test_result_id: int, output: str) -> Output:
        url = self._build_url("/api/v1/test_results/output")
        return self._create_with_http_template(
            url, UploadOutputDto(test_result_id=test_result_id, text=output), Output
        )

    def heartbeat_test(self, run_id: int, test_identifier: TestIdentifier) -> None:
        url = self._build_url(
            f"/api/v1/test_heartbeats/run/{run_id}/{test_identifier.suite_name}/{test_identifier.test_name}"
        )
        response = self._http_template.post_for_entity(url, {}, TestHeartbeat)
        if response.status_code() != 200:
            raise ValueError(f"Something went wrong when sending heartbeat: {response}")

    def start_test(self, start_test_dto: StartTestResultDto) -> None:
        url = self._build_url("/api/v1/test_results/start")
        response = self._http_template.post_for_entity(
            url, start_test_dto, StartTestResultDto
        )
        if response.status_code() != 200:
            raise ValueError(
                f"Something went wrong when starting test: {response.status_code()}, {response.text()}"
            )

    def finish_test(
        self,
        test_result_id: int,
        status: ResultStatus,
        seconds: float,
        message: str,
        image_output: Optional[int] = None,
        reference_image: Optional[int] = None,
        diff_image: Optional[int] = None,
        error_value: Optional[float] = None,
        failure_reason: Optional[TestFailureReason] = None,
    ) -> None:
        url = self._build_url("/api/v1/test_results/finish")
        dto = FinishTestResultDto(
            id=test_result_id,
            status=status.value,
            seconds=seconds,
            message=message,
            image_output=image_output,
            reference_image=reference_image,
            diff_image=diff_image,
            error_value=error_value,
            failure_reason=failure_reason.value if failure_reason else None,
        )
        response = self._http_template.post_for_entity(url, dto, FinishTestResultDto)
        if response.status_code() != 200:
            raise ValueError(
                f"Something went wrong when finishing test: {response.status_code()}, {response.text()}"
            )

    def generate_run_url(self, project_id: int, run_id: int) -> str:
        return f"{self._url}/projects/{project_id}/runs/{run_id}"

    def get_test_results_by_run_id_and_test_status(
        self, run_id: int, test_status: UnifiedTestStatus
    ) -> Optional[List[TestIdentifier]]:
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

    def get_test_edits_to_sync_for_run(self, run_id: int) -> List[AbstractTestEdit]:
        url = self._build_url("/api/v1/test_edits/runs/{}/edits-to-sync".format(run_id))
        response = self._http_template.get_for_entity(url, List[Dict])
        if response.status_code() == 404:
            return []
        if response.status_code() == 200:
            dict_list = response.get_entities()
            entity_list = []
            for d in dict_list:
                if d["editType"] == "COMPARISON_SETTINGS":
                    entity_list.append(
                        self._object_mapper.from_dict(d, ComparisonSettingsEdit)
                    )
                elif d["editType"] == "REFERENCE_IMAGE":
                    entity_list.append(
                        self._object_mapper.from_dict(d, ReferenceImageEdit)
                    )
                else:
                    raise ValueError("Unsupported edit type: {}".format(d["editType"]))
            return entity_list
        self._raise_bad_parameters(response)

    def _build_url(self, url):
        return self._url + quote(url)

    def _get_json(self, reponse):
        return reponse.json()

    def _create_with_http_template(self, url: str, body: T, response_cls: Type[R]) -> R:
        response = self._http_template.post_for_entity(url, body, response_cls)
        if response.status_code() == 201:
            return response.get_entity()
        self._raise_bad_parameters(response)

    def _patch_with_http_template(self, url, body, response_cls):
        response = self._http_template.patch_for_entity(url, body, response_cls)
        if response.status_code() == 200:
            return response.get_entity()
        self._raise_bad_parameters(response)

    def _create_value_error_for_bad_request(self, response):
        return ValueError(
            "Bad parameters: {}".format(
                " ".join(
                    [
                        "{}: {}".format(key, value)
                        for key, value in response.get_json().items()
                    ]
                )
            )
        )

    def _find_with_http_template(self, url: str, response_cls: Type[T]) -> Optional[T]:
        response = self._http_template.get_for_entity(url, response_cls)
        if response.status_code() == 404:
            return None
        if response.status_code() == 200:
            return response.get_entity()
        self._raise_bad_parameters(response)

    def _find_many_with_http_template(
        self, url: str, response_cls: Type[T]
    ) -> Optional[List[T]]:
        response = self._http_template.get_for_entity(url, response_cls)
        if response.status_code() == 404:
            return None
        if response.status_code() == 200:
            return response.get_entities()
        self._raise_bad_parameters(response)

    def _raise_bad_parameters(self, response):
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
