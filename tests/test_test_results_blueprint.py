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


def test_get_test_result_output_should_return(client, test_result, output):
    url = "/api/v1/test_results/{}/output".format(test_result.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.get_json() == {
        "id": 1,
        "test_result_id": 1,
        "text": "This is a long text",
    }


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


def test_get_test_result_by_run_and_identifier_success(
    client, suite_result, test_result
):
    rv = client.get(
        f"/api/v1/test_results/runs/{suite_result.run_id}/{suite_result.suite_name}/{test_result.test_name}"
    )

    assert rv.status_code == 200
    assert rv.get_json() == {
        "execution_status": "NOT_STARTED",
        "finished_at": test_result.finished_at.isoformat(),
        "id": 1,
        "image_output": 1,
        "machine_info": {"cores": 56, "cpu_name": "cpu", "memory": 8},
        "message": "sucess",
        "reference_image": 1,
        "seconds": 5.0,
        "started_at": test_result.started_at.isoformat(),
        "status": "SUCCESS",
        "suite_result_id": 1,
        "test_command": "my_command",
        "test_identifier": "my_suite/my_test_name",
        "test_name": "my_test_name",
        "test_variables": {"testkey": "test_value"},
    }


def test_get_test_result_by_run_and_identifier_should_fail_invalid_run_id(client):
    rv = client.get("/api/v1/test_results/runs/10/suite_name/test_name")

    assert rv.status_code == 404


def test_get_test_result_by_run_and_identifier_should_fail_invalid_test_identifier(
    client, suite_result
):
    rv = client.get(f"/api/v1/test_results/runs/{suite_result.run_id}/sdrft/test_name")

    assert rv.status_code == 404


def test_update_test_result_success(client, test_result):
    rv = client.patch(
        f"/api/v1/test_results/{test_result.id}", json={"status": "FAILED"}
    )

    assert rv.get_json() == {
        "execution_status": "NOT_STARTED",
        "finished_at": test_result.finished_at.isoformat(),
        "id": 1,
        "image_output": 1,
        "machine_info": {"cores": 56, "cpu_name": "cpu", "memory": 8},
        "message": "sucess",
        "reference_image": 1,
        "seconds": 5.0,
        "started_at": test_result.started_at.isoformat(),
        "status": "FAILED",
        "suite_result_id": 1,
        "test_command": "my_command",
        "test_identifier": "my_suite/my_test_name",
        "test_name": "my_test_name",
        "test_variables": {"testkey": "test_value"},
    }
    assert rv.status_code == 200


def test_update_test_result_failure_invalid_data(client, test_result):
    rv = client.patch(
        f"/api/v1/test_results/{test_result.id}", json={"status": "sdfsdf"}
    )

    assert rv.get_json() == {"status": ["Invalid enum member sdfsdf"]}
    assert rv.status_code == 400


def test_update_test_result_failure_invalid_test_result_id(client):
    rv = client.patch("/api/v1/test_results/42", json={"status": "SUCCESS"})

    assert rv.status_code == 404


def test_create_output_success(client, test_result):
    rv = client.post(
        "/api/v1/test_results/output",
        json={"test_result_id": test_result.id, "text": "my text"},
    )

    assert rv.status_code == 201
    assert rv.get_json() == {
        "id": 1,
        "test_result_id": test_result.id,
        "text": "my text",
    }


def test_create_output_failure(client, test_result):
    rv = client.post(
        "/api/v1/test_results/output", json={"test_result_id": 42, "text": "my text"}
    )

    assert rv.status_code == 400
    assert rv.get_json() == {"test_result_id": ["No test result exists for id 42."]}
