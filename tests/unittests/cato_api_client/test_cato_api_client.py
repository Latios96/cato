import datetime
import os

import pytest
from requests.models import Response

from cato_server.domain.image import Image, ImageChannel
from cato_server.domain.machine_info import MachineInfo
from cato_server.domain.output import Output
from cato_server.domain.project import Project
from cato_server.domain.run import Run
from cato_server.domain.test_identifier import TestIdentifier
from cato.domain.test_status import TestStatus
from cato_server.domain.file import File
from cato_server.domain.execution_status import ExecutionStatus
from cato_server.domain.suite_result import SuiteResult
from cato_server.domain.test_result import TestResult
from cato_api_client.cato_api_client import CatoApiClient
from cato_api_client.http_template import AbstractHttpTemplate, HttpTemplateResponse
from cato_api_models.catoapimodels import (
    CreateFullRunDto,
    TestSuiteForRunCreation,
    TestForRunCreation,
    MachineInfoDto,
)
from cato_server.domain.submission_info import SubmissionInfo


class FlaskClientHttpTemplateResponse(HttpTemplateResponse):
    def __init__(self, response, response_cls, mapper) -> None:
        super(FlaskClientHttpTemplateResponse, self).__init__(response_cls, mapper)
        self._response = response

    def status_code(self) -> int:
        return self._response.status_code

    def get_json(self):
        return self._response.get_json()

    def text(self):
        return self._response.data


class FlaskClientHttpTemplate(AbstractHttpTemplate):
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
        return FlaskClientHttpTemplateResponse(
            response, response_cls, self._object_mapper
        )


class CatoApiTestClient(CatoApiClient):
    def __init__(self, url, client, object_mapper):
        super(CatoApiTestClient, self).__init__(
            url, FlaskClientHttpTemplate(client, object_mapper), object_mapper
        )
        self._client = client

    def _get(self, url: str) -> Response:
        get = self._client.get(url.replace(self._url, ""))
        return get

    def _post_form(self, url, params, files=None):
        if files:
            params.update(files)
        return self._client.post(url.replace(self._url, ""), data=params)

    def _post_json(self, url, params):
        return self._client.post(url.replace(self._url, ""), json=params)

    def _get_json(self, reponse):
        return reponse.get_json()

    def _get_url(self, url):
        return self._client.get(url.replace(self._url, ""))


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
        cato_api_client.create_project("my project")


def test_upload_file(cato_api_client, test_resource_provider):
    path = test_resource_provider.resource_by_name("test.exr")

    f = cato_api_client.upload_file(path)

    assert f == File(
        id=1,
        name="test.png",
        hash="505cc9e0719a4f15a36eaa6df776bea0cc065b32d198be6002a79a03823b4d9e",
        value_counter=0,
    )


def test_upload_file_not_existing(cato_api_client):
    path = os.path.join(os.path.dirname(__file__), "seAERER")

    with pytest.raises(ValueError):
        cato_api_client.upload_file(path)


def test_create_suite_result_success(cato_api_client, run):
    suite_result = SuiteResult(
        id=0, run_id=run.id, suite_name="my_suite", suite_variables={"key": "value"}
    )

    result = cato_api_client.create_suite_result(suite_result)

    assert result == SuiteResult(
        id=1, run_id=run.id, suite_name="my_suite", suite_variables={"key": "value"}
    )


def test_create_suite_result_failure_missing_run_id(cato_api_client, run):
    suite_result = SuiteResult(
        id=0, run_id=42, suite_name="my_suite", suite_variables={"key": "value"}
    )

    with pytest.raises(ValueError):
        cato_api_client.create_suite_result(suite_result)


def test_create_run_success(cato_api_client, project):
    started_at = datetime.datetime.now()
    run = Run(id=0, project_id=project.id, started_at=started_at)

    result = cato_api_client.create_run(run)

    assert result == Run(id=1, project_id=project.id, started_at=started_at)


def test_create_run_failure(cato_api_client):
    started_at = datetime.datetime.now()
    run = Run(id=0, project_id=2, started_at=started_at)

    with pytest.raises(ValueError):
        cato_api_client.create_run(run)


def test_create_test_result_success_minimal(cato_api_client, suite_result):
    test_result = TestResult(
        id=0,
        suite_result_id=suite_result.id,
        test_name="test",
        test_identifier=TestIdentifier(suite_result.suite_name, "test"),
        test_variables={},
        test_command="my_command",
        machine_info=MachineInfo(cpu_name="Intel Xeon", cores=8, memory=24),
    )

    result = cato_api_client.create_test_result(test_result)

    assert result == TestResult(
        id=1,
        suite_result_id=suite_result.id,
        test_name="test",
        test_identifier=TestIdentifier(suite_result.suite_name, "test"),
        test_variables={},
        test_command="my_command",
        machine_info=MachineInfo(cpu_name="Intel Xeon", cores=8, memory=24),
        execution_status=ExecutionStatus.NOT_STARTED,
        seconds=0,
    )


def test_create_test_result_success_complex(
    cato_api_client, suite_result, stored_image
):
    started_at = datetime.datetime.now()
    test_result = TestResult(
        id=0,
        suite_result_id=suite_result.id,
        test_name="test",
        test_identifier=TestIdentifier(suite_result.suite_name, "test"),
        test_variables={},
        test_command="my_command",
        machine_info=MachineInfo(cpu_name="Intel Xeon", cores=8, memory=24),
        started_at=started_at,
        image_output=stored_image.id,
    )

    result = cato_api_client.create_test_result(test_result)

    assert result == TestResult(
        id=1,
        suite_result_id=suite_result.id,
        test_name="test",
        test_identifier=TestIdentifier(suite_result.suite_name, "test"),
        test_variables={},
        test_command="my_command",
        machine_info=MachineInfo(cpu_name="Intel Xeon", cores=8, memory=24),
        execution_status=ExecutionStatus.NOT_STARTED,
        seconds=0,
        started_at=started_at,
        image_output=stored_image.id,
    )


def test_create_failure_failure(cato_api_client, suite_result):
    test_result = TestResult(
        id=0,
        suite_result_id=5,
        test_name="test",
        test_identifier=TestIdentifier(suite_result.suite_name, "test"),
        test_variables={},
        test_command="my_command",
        machine_info=MachineInfo(cpu_name="Intel Xeon", cores=8, memory=24),
    )

    with pytest.raises(ValueError):
        cato_api_client.create_test_result(test_result)


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
        execution_status=ExecutionStatus.NOT_STARTED,
        status=TestStatus.SUCCESS,
        seconds=5,
        message="success",
        image_output=1,
        reference_image=1,
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


def test_update_test_result(cato_api_client, test_result):
    test_result.status = TestStatus.FAILED

    result = cato_api_client.update_test_result(test_result)

    assert result == test_result


def test_update_test_failure(cato_api_client, test_result):
    test_result.reference_image = 42

    with pytest.raises(ValueError):
        cato_api_client.update_test_result(test_result)


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
        width=2046,
        height=1554,
    )


def test_upload_image_not_existing(cato_api_client):
    path = os.path.join(os.path.dirname(__file__), "seAERER")

    with pytest.raises(ValueError):
        cato_api_client.upload_image(path)


def test_create_full_run_success(cato_api_client, project):
    dto = CreateFullRunDto(
        project_id=project.id,
        test_suites=[
            TestSuiteForRunCreation(
                suite_name="my_suite",
                suite_variables={},
                tests=[
                    TestForRunCreation(
                        machine_info=MachineInfoDto(cpu_name="test", cores=8, memory=8),
                        test_command="cmd",
                        test_identifier="test/identifier",
                        test_name="test_name",
                        test_variables={},
                    )
                ],
            )
        ],
    )
    run = cato_api_client.create_full_run(dto)
    assert run.id == project.id


def test_create_full_run_failure(cato_api_client):
    dto = CreateFullRunDto(
        project_id=42,
        test_suites=[
            TestSuiteForRunCreation(
                suite_name="my_suite",
                suite_variables={},
                tests=[
                    TestForRunCreation(
                        MachineInfoDto(cpu_name="test", cores=8, memory=8),
                        "cmd",
                        "test/identifier",
                        "test_name",
                        {},
                    )
                ],
            )
        ],
    )
    with pytest.raises(ValueError):
        cato_api_client.create_full_run(dto)


def test_send_test_heartbeat(cato_api_client, run, test_result):
    cato_api_client.heartbeat_test(run.id, test_result.test_identifier)


def test_send_test_heartbeat_not_existing_test_id(cato_api_client):
    with pytest.raises(ValueError):
        cato_api_client.heartbeat_test(42, TestIdentifier("suite_name", "test_name"))


def test_finish_test_result_success(cato_api_client, test_result, stored_image):
    cato_api_client.finish_test(
        test_result_id=test_result.id,
        status=TestStatus.SUCCESS,
        seconds=3,
        message="my_mesage",
        image_output=stored_image.id,
        reference_image=stored_image.id,
    )


def test_finish_test_result_failure(cato_api_client, test_result, stored_image):
    with pytest.raises(ValueError):
        cato_api_client.finish_test(
            test_result_id=test_result.id,
            status=TestStatus.SUCCESS,
            seconds=3,
            message="my_mesage",
            image_output=42,
            reference_image=stored_image.id,
        )


def test_get_test_results_by_run_id_and_test_status_should_find(
    cato_api_client, run, test_result
):
    identifiers = cato_api_client.get_test_results_by_run_id_and_test_status(
        run.id, TestStatus.SUCCESS
    )

    assert identifiers == [test_result.test_identifier]


def test_get_test_results_by_run_id_and_test_status_should_not_find(
    cato_api_client, run, test_result
):
    identifiers = cato_api_client.get_test_results_by_run_id_and_test_status(
        run.id, TestStatus.FAILED
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
