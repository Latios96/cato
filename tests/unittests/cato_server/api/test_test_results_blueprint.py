import datetime


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
    json = rv.json()
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
    json = rv.json()
    assert len(json) == 1
    assert json[0]["id"] == 1
    assert json[0].get("output") is None


def test_get_test_result_by_suite_id_should_return_empty_list(
    client, suite_result, test_result
):
    url = "/api/v1/test_results/suite_result/42".format(suite_result_id=suite_result.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == []


def test_get_test_result_output_should_return(client, test_result, output):
    url = "/api/v1/test_results/{}/output".format(test_result.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "id": 1,
        "test_result_id": 1,
        "text": "This is a long text",
    }


def test_get_test_result_output_should_404(client, test_result):
    url = "/api/v1/test_results/42/output"

    rv = client.get(url)

    assert rv.status_code == 404


def test_create_test_result_success(client, suite_result, stored_image):
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
            "image_output": stored_image.id,
            "reference_image": stored_image.id,
            "started_at": started_at,
            "finished_at": finished_at,
        },
    )

    assert rv.json() == {
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

    assert rv.json() == {"suite_result_id": ["No suite result exists for id 5."]}
    assert rv.status_code == 400


def test_get_test_result_by_run_and_identifier_success(
    client, suite_result, test_result
):
    rv = client.get(
        f"/api/v1/test_results/runs/{suite_result.run_id}/{suite_result.suite_name}/{test_result.test_name}"
    )

    assert rv.status_code == 200
    assert rv.json() == {
        "execution_status": "NOT_STARTED",
        "finished_at": test_result.finished_at.isoformat(),
        "id": 1,
        "image_output": 1,
        "machine_info": {"cores": 56, "cpu_name": "cpu", "memory": 8},
        "message": "success",
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


def test_create_output_success(client, test_result):
    rv = client.post(
        "/api/v1/test_results/output",
        json={"test_result_id": test_result.id, "text": "my text"},
    )

    assert rv.status_code == 201
    assert rv.json() == {
        "id": 1,
        "test_result_id": test_result.id,
        "text": "my text",
    }


def test_create_output_failure(client, test_result):
    rv = client.post(
        "/api/v1/test_results/output", json={"test_result_id": 42, "text": "my text"}
    )

    assert rv.status_code == 400
    assert rv.json() == {"test_result_id": ["No test result exists for id 42."]}


def test_get_test_results_by_run_id_should_find(client, run, test_result):
    url = f"/api/v1/test_results/run/{run.id}"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == [
        {
            "execution_status": "NOT_STARTED",
            "id": 1,
            "name": "my_test_name",
            "status": "SUCCESS",
            "test_identifier": "my_suite/my_test_name",
        }
    ]


def test_get_test_results_by_run_id_should_return_empty_list(client):
    url = f"/api/v1/test_results/run/{42}"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == []


def test_get_test_results_by_run_id_paginated_should_find(client, run, test_result):
    url = f"/api/v1/test_results/run/{run.id}?page_number=1&page_size=10"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "page_number": 1,
        "page_size": 10,
        "total_entity_count": 1,
        "entities": [
            {
                "execution_status": "NOT_STARTED",
                "id": 1,
                "name": "my_test_name",
                "status": "SUCCESS",
                "test_identifier": "my_suite/my_test_name",
            }
        ],
    }


def test_get_test_results_by_run_id_paginated_should_return_empty_page(client):
    url = f"/api/v1/test_results/run/{42}?page_number=1&page_size=10"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "page_number": 1,
        "page_size": 10,
        "total_entity_count": 0,
        "entities": [],
    }


def test_get_test_result_by_id(client, test_result):
    url = f"/api/v1/test_results/{test_result.id}"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "execution_status": "NOT_STARTED",
        "finished_at": test_result.finished_at.isoformat(),
        "id": 1,
        "diff_image": {
            "channels": [
                {"file_id": 1, "id": 1, "name": "rgb"},
                {"file_id": 2, "id": 2, "name": "alpha"},
            ],
            "height": 1080,
            "id": 1,
            "name": "test.exr",
            "original_file_id": 1,
            "width": 1920,
        },
        "image_output": {
            "channels": [
                {"file_id": 1, "id": 1, "name": "rgb"},
                {"file_id": 2, "id": 2, "name": "alpha"},
            ],
            "id": 1,
            "name": "test.exr",
            "original_file_id": 1,
            "width": 1920,
            "height": 1080,
        },
        "machine_info": {"cores": 56, "cpu_name": "cpu", "memory": 8},
        "message": "success",
        "reference_image": {
            "channels": [
                {"file_id": 1, "id": 1, "name": "rgb"},
                {"file_id": 2, "id": 2, "name": "alpha"},
            ],
            "id": 1,
            "name": "test.exr",
            "original_file_id": 1,
            "width": 1920,
            "height": 1080,
        },
        "seconds": 5.0,
        "started_at": test_result.started_at.isoformat(),
        "status": "SUCCESS",
        "suite_result_id": 1,
        "test_command": "my_command",
        "test_identifier": "my_suite/my_test_name",
        "test_name": "my_test_name",
        "test_variables": {"testkey": "test_value"},
    }


def test_get_test_result_by_id_no_machine_info_no_diff_image(
    client, test_result_no_machine_info
):
    url = f"/api/v1/test_results/{test_result_no_machine_info.id}"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "execution_status": "NOT_STARTED",
        "finished_at": test_result_no_machine_info.finished_at.isoformat(),
        "id": 1,
        "diff_image": None,
        "image_output": {
            "channels": [
                {"file_id": 1, "id": 1, "name": "rgb"},
                {"file_id": 2, "id": 2, "name": "alpha"},
            ],
            "id": 1,
            "name": "test.exr",
            "original_file_id": 1,
            "width": 1920,
            "height": 1080,
        },
        "machine_info": None,
        "message": "success",
        "reference_image": {
            "channels": [
                {"file_id": 1, "id": 1, "name": "rgb"},
                {"file_id": 2, "id": 2, "name": "alpha"},
            ],
            "id": 1,
            "name": "test.exr",
            "original_file_id": 1,
            "width": 1920,
            "height": 1080,
        },
        "seconds": 5.0,
        "started_at": test_result_no_machine_info.started_at.isoformat(),
        "status": "SUCCESS",
        "suite_result_id": 1,
        "test_command": "my_command",
        "test_identifier": "my_suite/my_test_name",
        "test_name": "my_test_name",
        "test_variables": {"testkey": "test_value"},
    }


def test_get_test_results_by_run_id_should_404(client):
    url = f"/api/v1/test_results/{42}"

    rv = client.get(url)

    assert rv.status_code == 404


def test_finish_test_success(client, test_result, stored_image):
    url = "/api/v1/test_results/finish"
    data = {
        "id": test_result.id,
        "status": "SUCCESS",
        "seconds": 3,
        "message": "this is my finishing message",
        "image_output": stored_image.id,
        "reference_image": stored_image.id,
    }
    rv = client.post(url, json=data)

    assert rv.status_code == 200


def test_finish_test_failure(client, test_result, stored_image):
    url = "/api/v1/test_results/finish"
    data = {
        "id": test_result.id,
        "status": "SUCCESS",
        "seconds": 3,
        "message": "this is my finishing message",
        "image_output": 42,
        "reference_image": stored_image.id,
    }
    rv = client.post(url, json=data)

    assert rv.status_code == 400
    assert rv.json() == {"image_output": ["No image exists for id 42."]}


def test_should_find_by_run_id_and_test_status(client, run, test_result):
    url = f"/api/v1/test_results/run/{run.id}/test_status/SUCCESS"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == [{"suite_name": "my_suite", "test_name": "my_test_name"}]


def test_should_not_find_by_run_id_and_test_status(client, run, test_result):
    url = f"/api/v1/test_results/run/{run.id}/test_status/FAILED"

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == []


def test_invalid_test_status(client, run, test_result):
    url = f"/api/v1/test_results/run/{run.id}/test_status/dd"

    rv = client.get(url)

    assert rv.status_code == 400
    assert rv.json() == {"test_status": "Not a valid test status: dd."}


def test_start_test_success(client, test_result):
    url = "/api/v1/test_results/start"
    data = {
        "id": test_result.id,
        "machine_info": {
            "cpu_name": "test",
            "cores": 8,
            "memory": 8,
        },
    }
    rv = client.post(url, json=data)

    assert rv.status_code == 200


def test_start_test_failure(client):
    url = "/api/v1/test_results/start"
    data = {
        "id": 42,
        "machine_info": {
            "cpu_name": "test",
            "cores": 8,
            "memory": 8,
        },
    }
    rv = client.post(url, json=data)

    assert rv.status_code == 400
    assert rv.json() == {"id": ["No TestResult with id 42 exists!"]}
