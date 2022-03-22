import datetime
import os
from typing import Dict, Type, Optional

import pytest
from requests.models import Response

from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings
from cato_api_client.cato_api_client import CatoApiClient
from cato_api_client.http_template import AbstractHttpTemplate, HttpTemplateResponse, R
from cato_common.domain.branch_name import BranchName
from cato_common.domain.compare_image_result import CompareImageResult
from cato_common.domain.file import File
from cato_common.domain.image import Image, ImageChannel
from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.output import Output
from cato_common.domain.project import Project
from cato_common.domain.submission_info import SubmissionInfo
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.test_result import TestResult
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.dtos.create_full_run_dto import (
    CreateFullRunDto,
    TestSuiteForRunCreation,
    TestForRunCreation,
)
from cato_common.dtos.start_test_result_dto import StartTestResultDto


class FastApiClientHttpTemplateResponse(HttpTemplateResponse):
    def __init__(self, response, response_cls, mapper) -> None:
        super(FastApiClientHttpTemplateResponse, self).__init__(response_cls, mapper)
        self._response = response

    def status_code(self) -> int:
        return self._response.status_code

    def get_json(self):
        return self._response.json()

    def text(self):
        return self._response.text

    def content(self):
        return self._response.content


class FastApiClientHttpTemplate(AbstractHttpTemplate):
    def __init__(self, client, object_mapper):
        self._client = client
        self._object_mapper = object_mapper

    def _post(self, url, params):
        return self._client.post(url, json=params)

    def _get(self, url):
        return self._client.get(url)

    def _patch(self, url, params):
        return self._client.patch(url, json=params)

    def _construct_http_template_response(self, response, response_cls):
        return FastApiClientHttpTemplateResponse(
            response, response_cls, self._object_mapper
        )

    def post_files_for_entity(
        self, url: str, body: Optional, files: Dict[str, str], response_cls: Type[R]
    ) -> HttpTemplateResponse[R]:
        response = self._client.post(url, data=body, files=files)
        return self._construct_http_template_response(response, response_cls)


class CatoApiTestClient(CatoApiClient):
    def __init__(self, url, client, object_mapper):
        super(CatoApiTestClient, self).__init__(
            url, FastApiClientHttpTemplate(client, object_mapper), object_mapper
        )
        self._client = client

    def _get(self, url: str) -> Response:
        get = self._client.get(url.replace(self._url, ""))
        return get

    def _post_form(self, url, params, files=None):
        return self._client.post(url.replace(self._url, ""), data=params, files=files)

    def _post_json(self, url, params):
        return self._client.post(url.replace(self._url, ""), json=params)

    def _get_json(self, reponse):
        return reponse.json()


@pytest.fixture
def cato_api_client(app_and_config_fixture, client, object_mapper):
    pp, config = app_and_config_fixture
    api_client = CatoApiTestClient(
        f"http://localhost:{config.port}", client, object_mapper
    )
    return api_client


def test_get_project_by_name_should_get_project(cato_api_client, project):
    project = cato_api_client.get_project_by_name("test_name")

    assert project == Project(1, "test_name")


def test_get_project_by_name_should_get_none(cato_api_client):
    project = cato_api_client.get_project_by_name("ysdf")

    assert project is None


def test_create_project_should_create_project(cato_api_client):
    project = cato_api_client.create_project("my_project")

    assert project == Project(id=1, name="my_project")


def test_create_project_should_not_create_invalid_name(cato_api_client):
    with pytest.raises(ValueError):
        cato_api_client.create_project("my%&&&project")


def test_upload_file(cato_api_client, test_resource_provider):
    path = test_resource_provider.resource_by_name("test.exr")

    f = cato_api_client.upload_file(path)

    assert f == File(
        id=1,
        name="test.exr",
        hash="a233c347f49d2745b4f759bec0da9414e1bc980b1ece56f98dd7f9696d608709",
        value_counter=0,
    )


def test_upload_file_not_existing(cato_api_client):
    path = os.path.join(os.path.dirname(__file__), "seAERER")

    with pytest.raises(ValueError):
        cato_api_client.upload_file(path)


def test_get_test_result_by_run_and_identifier_success(
    cato_api_client, suite_result, test_result
):
    result = cato_api_client.find_test_result_by_run_id_and_identifier(
        suite_result.run_id,
        TestIdentifier(suite_result.suite_name, test_result.test_name),
    )

    assert result == TestResult(
        id=1,
        suite_result_id=suite_result.id,
        test_name="my_test_name",
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test_name"),
        test_command="my_command",
        test_variables={"testkey": "test_value"},
        machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
        unified_test_status=UnifiedTestStatus.NOT_STARTED,
        seconds=5,
        message="success",
        image_output=1,
        reference_image=1,
        diff_image=1,
        started_at=test_result.started_at,
        finished_at=test_result.finished_at,
    )


def test_get_test_result_by_run_and_identifier_should_fail_invalid_run_id(
    cato_api_client, suite_result, test_result
):
    result = cato_api_client.find_test_result_by_run_id_and_identifier(
        10, TestIdentifier(suite_result.suite_name, test_result.test_name)
    )

    assert result is None


def test_get_test_result_by_run_and_identifier_should_fail_invalid_test_identifier(
    cato_api_client, suite_result
):
    result = cato_api_client.find_test_result_by_run_id_and_identifier(
        suite_result.run_id, TestIdentifier("test", "wurst")
    )

    assert result is None


def test_upload_output_success(cato_api_client, test_result):
    output = cato_api_client.upload_output(test_result.id, "my text")

    assert output == Output(id=1, test_result_id=test_result.id, text="my text")


def test_upload_output_failure(cato_api_client):
    with pytest.raises(ValueError):
        cato_api_client.upload_output(42, "my text")


def test_upload_image(cato_api_client, test_resource_provider):
    path = test_resource_provider.resource_by_name("test.exr")

    f = cato_api_client.upload_image(path)

    assert f == Image(
        id=1,
        name="test.exr",
        original_file_id=1,
        channels=[ImageChannel(id=1, image_id=1, name="rgb", file_id=2)],
        width=2048,
        height=1556,
    )


def test_upload_image_not_existing(cato_api_client):
    path = os.path.join(os.path.dirname(__file__), "seAERER")

    with pytest.raises(ValueError):
        cato_api_client.upload_image(path)


def test_create_run_success(cato_api_client, project):
    dto = CreateFullRunDto(
        project_id=project.id,
        test_suites=[
            TestSuiteForRunCreation(
                suite_name="my_suite",
                suite_variables={},
                tests=[
                    TestForRunCreation(
                        test_command="cmd",
                        test_identifier=TestIdentifier.from_string("test/identifier"),
                        test_name="test_name",
                        test_variables={},
                        comparison_settings=ComparisonSettings.default(),
                    )
                ],
            )
        ],
        branch_name=BranchName("default"),
    )
    run = cato_api_client.create_run(dto)
    assert run.id == project.id


def test_create_run_failure(cato_api_client):
    dto = CreateFullRunDto(
        project_id=42,
        test_suites=[
            TestSuiteForRunCreation(
                suite_name="my_suite",
                suite_variables={},
                tests=[
                    TestForRunCreation(
                        test_command="cmd",
                        test_identifier=TestIdentifier.from_string("test/identifier"),
                        test_name="test_name",
                        test_variables={},
                        comparison_settings=ComparisonSettings.default(),
                    )
                ],
            )
        ],
        branch_name=BranchName("default"),
    )
    with pytest.raises(ValueError):
        cato_api_client.create_run(dto)


def test_send_test_heartbeat(cato_api_client, run, test_result):
    cato_api_client.heartbeat_test(run.id, test_result.test_identifier)


def test_send_test_heartbeat_not_existing_test_id(cato_api_client):
    with pytest.raises(ValueError):
        cato_api_client.heartbeat_test(42, TestIdentifier("suite_name", "test_name"))


def test_finish_test_result_success(cato_api_client, test_result, stored_image_factory):
    cato_api_client.finish_test(
        test_result_id=test_result.id,
        status=ResultStatus.SUCCESS,
        seconds=3,
        message="my_mesage",
        image_output=stored_image_factory().id,
        reference_image=stored_image_factory().id,
        diff_image=stored_image_factory().id,
    )


def test_finish_test_result_failure(cato_api_client, test_result, stored_image):
    with pytest.raises(ValueError):
        cato_api_client.finish_test(
            test_result_id=test_result.id,
            status=ResultStatus.SUCCESS,
            seconds=3,
            message="my_mesage",
            image_output=42,
            reference_image=stored_image.id,
            failure_reason=TestFailureReason.TIMED_OUT,
        )


def test_get_test_results_by_run_id_and_test_status_should_find(
    cato_api_client, run, test_result
):
    identifiers = cato_api_client.get_test_results_by_run_id_and_test_status(
        run.id, UnifiedTestStatus.NOT_STARTED
    )

    assert identifiers == [test_result.test_identifier]


def test_get_test_results_by_run_id_and_test_status_should_not_find(
    cato_api_client, run, test_result
):
    identifiers = cato_api_client.get_test_results_by_run_id_and_test_status(
        run.id, ResultStatus.FAILED
    )

    assert identifiers == []


def test_run_id_exists_success(cato_api_client, run):
    assert cato_api_client.run_id_exists(run.id)


def test_run_id_exists_failure(cato_api_client):
    assert not cato_api_client.run_id_exists(42)


def test_submit_to_scheduler_success(cato_api_client, config_fixture, run):
    submission_info = SubmissionInfo(
        id=0,
        config=config_fixture.CONFIG,
        run_id=run.id,
        resource_path="resource_path",
        executable=r"python.exe",
    )

    cato_api_client.submit_to_scheduler(submission_info)


def test_find_submission_info_by_id(cato_api_client, submission_info):
    found_info = cato_api_client.get_submission_info_by_id(submission_info.id)

    assert found_info == submission_info


def test_find_submission_info_by_not_existing_id(cato_api_client):
    found_info = cato_api_client.get_submission_info_by_id(42)

    assert found_info == None


def test_start_test_success(cato_api_client, test_result):
    cato_api_client.start_test(
        StartTestResultDto(
            id=test_result.id,
            machine_info=MachineInfo(cpu_name="Intel", cores=1, memory=1),
        )
    )


def test_start_test_failure(cato_api_client):
    with pytest.raises(ValueError):
        cato_api_client.start_test(
            StartTestResultDto(
                id=43, machine_info=MachineInfo(cpu_name="Intel", cores=1, memory=1)
            )
        )


def test_compare_images_success(cato_api_client, test_resource_provider):
    result = cato_api_client.compare_images(
        test_resource_provider.resource_by_name("test_image_white.jpg"),
        test_resource_provider.resource_by_name("test_image_white.jpg"),
        ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1),
    )

    assert result == CompareImageResult(
        status=ResultStatus.SUCCESS,
        message=None,
        reference_image_id=2,
        output_image_id=1,
        diff_image_id=3,
        error=1,
    )


def test_compare_images_success_should_fail_for_not_existing_reference_image(
    cato_api_client, test_resource_provider
):
    with pytest.raises(ValueError):
        cato_api_client.compare_images(
            "not_existing.jpg",
            test_resource_provider.resource_by_name("test_image_black.png"),
            ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1),
        )


def test_compare_images_success_should_fail_for_not_existing_output_image(
    cato_api_client, test_resource_provider
):
    with pytest.raises(ValueError):
        cato_api_client.compare_images(
            test_resource_provider.resource_by_name("test_image_black.png"),
            "not_existing.jpg",
            ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1),
        )


def test_compare_images_success_should_fail_for_non_image(
    cato_api_client, test_resource_provider
):
    with pytest.raises(ValueError):
        cato_api_client.compare_images(
            test_resource_provider.resource_by_name("unsupported-file.txt"),
            test_resource_provider.resource_by_name("unsupported-file.txt"),
            ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1),
        )


def test_get_test_edits_to_sync_for_run_should_return_edits(
    cato_api_client,
    run,
    test_result,
    saving_comparison_settings_edit_factory,
    saving_reference_image_edit_factory,
):
    comparison_settings_edit = saving_comparison_settings_edit_factory(
        test_id=test_result.id,
        created_at=datetime.datetime.now() - datetime.timedelta(seconds=10),
    )
    reference_image_edit = saving_reference_image_edit_factory(
        test_id=test_result.id, created_at=datetime.datetime.now()
    )
    edits = cato_api_client.get_test_edits_to_sync_for_run(run.id)

    assert edits == [comparison_settings_edit, reference_image_edit]


def test_get_test_edits_to_sync_for_run_should_return_empty_list(cato_api_client, run):
    edits = cato_api_client.get_test_edits_to_sync_for_run(run.id)

    assert edits == []


def test_download_original_image_success(cato_api_client, stored_image):
    content = cato_api_client.download_original_image(stored_image.id)

    assert len(content) == 87444


def test_download_original_image_not_found(cato_api_client):
    content = cato_api_client.download_original_image(1)

    assert content is None


def test_get_image_by_id_success(cato_api_client, stored_image):
    image = cato_api_client.get_image_by_id(stored_image.id)

    assert image == stored_image


def test_get_image_by_id_not_found(cato_api_client):
    image = cato_api_client.get_image_by_id(42)

    assert image is None
