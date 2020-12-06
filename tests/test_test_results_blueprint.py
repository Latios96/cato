import datetime

import pytest


def test_get_test_result_by_suite_and_identifier_should_return(
    client, suite_result, test_result
):
    url = "/api/v1/test_results/suite_result/{suite_result_id}/{suite_name}/{test_name}".format(
        suite_result_id=suite_result.id,
        suite_name=suite_result.suite_name,
        test_name=test_result.test_name,
    )

    rv = client.get(url)

    assert rv.status_code == 200
    json = rv.get_json()
    assert json["id"] == 1
    assert json.get("output") is None


def test_get_test_result_by_suite_and_identifier_should_404(client):
    url = "/api/v1/test_results/suite_result/1/suite_name/test_name"

    rv = client.get(url)

    assert rv.status_code == 404


def test_get_test_result_by_suite_id_should_return(client, suite_result, test_result):
    url = "/api/v1/test_results/suite_result/{suite_result_id}".format(
        suite_result_id=suite_result.id
    )

    rv = client.get(url)

    assert rv.status_code == 200
    json = rv.get_json()
    assert len(json) == 1
    assert json[0]["id"] == 1
    assert json[0].get("output") is None


def test_get_test_result_by_suite_id_should_return_empty_list(
    client, suite_result, test_result
):
    url = "/api/v1/test_results/suite_result/42".format(suite_result_id=suite_result.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.get_json() == []


def test_get_test_result_output_should_return(client, test_result):
    url = "/api/v1/test_results/{}/output".format(test_result.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.get_json() == ["1", "2", "3"]


def test_get_test_result_output_should_404(client, test_result):
    url = "/api/v1/test_results/42/output"

    rv = client.get(url)

    assert rv.status_code == 404


def test_create_test_result_success(client, suite_result, stored_file):
    started_at = datetime.datetime.now().isoformat()
    finished_at = datetime.datetime.now().isoformat()
    rv = client.post(
        "/api/v1/test_results",
        json={
            "suite_result_id": 1,
            "test_name": "my_test_name",
            "test_identifier": "my_suite/my_test_name",
            "test_command": "my_command",
            "test_variables": {"key": "value"},
            "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
            "execution_status": "NOT_STARTED",
            "image_output": stored_file.id,
            "reference_image": stored_file.id,
            "started_at": started_at,
            "finished_at": finished_at,
        },
    )

    assert rv.get_json() == {
        "execution_status": "NOT_STARTED",
        "finished_at": finished_at,
        "id": 1,
        "image_output": 1,
        "machine_info": {"cores": 8, "cpu_name": "Intel", "memory": 24},
        "reference_image": 1,
        "seconds": 0,
        "started_at": started_at,
        "suite_result_id": 1,
        "test_command": "my_command",
        "test_identifier": "my_suite/my_test_name",
        "test_name": "my_test_name",
        "test_variables": {"key": "value"},
    }
    assert rv.status_code == 201


def test_create_test_result_failure(client, suite_result, stored_file):
    started_at = datetime.datetime.now().isoformat()
    finished_at = datetime.datetime.now().isoformat()
    rv = client.post(
        "/api/v1/test_results",
        json={
            "suite_result_id": 5,
            "test_name": "my_test_name",
            "test_identifier": "my_suite/test_identifier",
            "test_command": "my_command",
            "test_variables": {"key": "value"},
            "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
            "execution_status": "NOT_STARTED",
            "image_output": stored_file.id,
            "reference_image": stored_file.id,
            "started_at": started_at,
            "finished_at": finished_at,
        },
    )

    assert rv.get_json() == {"suite_result_id": ["No suite result exists for id 5."]}
    assert rv.status_code == 400
