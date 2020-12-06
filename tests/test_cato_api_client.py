import datetime
import os

import pytest
from requests.models import Response

from cato.domain import run
from cato.domain.machine_info import MachineInfo
from cato.domain.project import Project
from cato.domain.run import Run
from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_result import TestStatus
from cato.storage.domain.File import File
from cato.storage.domain.execution_status import ExecutionStatus
from cato.storage.domain.suite_result import SuiteResult
from cato.storage.domain.test_result import TestResult
from cato_api_client.cato_api_client import CatoApiClient


class CatoApiTestClient(CatoApiClient):
    def __init__(self, url, client):
        super(CatoApiTestClient, self).__init__(url)
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


@pytest.fixture
def cato_api_client(app_and_config_fixture, client):
    pp, config = app_and_config_fixture
    api_client = CatoApiTestClient(f"http://localhost:{config.port}", client)
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


def test_upload_file(cato_api_client):
    path = os.path.join(os.path.dirname(__file__), "test.exr")

    f = cato_api_client.upload_file(path)

    assert f == File(
        id=1,
        name="test.png",
        hash="505cc9e0719a4f15a36eaa6df776bea0cc065b32d198be6002a79a03823b4d9e",
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
        output=[],
    )


def test_create_test_result_success_complex(cato_api_client, suite_result, stored_file):
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
        image_output=stored_file.id,
        output=["1", "2", "3"],
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
        image_output=stored_file.id,
        output=["1", "2", "3"],
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
        id=0,
        suite_result_id=suite_result.id,
        test_name="my_test_name",
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test_name"),
        test_command="my_command",
        test_variables={"testkey": "test_value"},
        machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
        execution_status=ExecutionStatus.NOT_STARTED,
        status=TestStatus.SUCCESS,
        seconds=5,
        message="sucess",
        image_output=3,
        reference_image=4,
        started_at=test_result.started_at,
        finished_at=test_result.finished_at,
    )


def test_get_test_result_by_run_and_identifier_should_fail_invalid_run_id(
    cato_api_client, suite_result, test_result
):

    result = cato_api_client.find_test_result_by_run_id_and_identifier(
        10, TestIdentifier(suite_result.suite_name, test_result.test_name)
    )

    assert result == None


def test_get_test_result_by_run_and_identifier_should_fail_invalid_test_identifier(
    cato_api_client, suite_result
):

    result = cato_api_client.find_test_result_by_run_id_and_identifier(
        suite_result.run_id, TestIdentifier("test", "wurst")
    )

    assert result == None
