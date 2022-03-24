def test_get_test_result_by_suite_and_identifier_should_return(
    client_with_session, suite_result, test_result
):
    url = "/api/v1/test_results/suite_result/{suite_result_id}/{suite_name}/{test_name}".format(
        suite_result_id=suite_result.id,
        suite_name=suite_result.suite_name,
        test_name=test_result.test_name,
    )

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    json = rv.json()
    assert json["id"] == 1
    assert json.get("output") is None


def test_get_test_result_by_suite_and_identifier_should_404(client_with_session):
    url = "/api/v1/test_results/suite_result/1/suite_name/test_name"

    rv = client_with_session.get(url)

    assert rv.status_code == 404


def test_get_test_result_by_suite_id_should_return(
    client_with_session, suite_result, test_result
):
    url = "/api/v1/test_results/suite_result/{suite_result_id}".format(
        suite_result_id=suite_result.id
    )

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    json = rv.json()
    assert len(json) == 1
    assert json[0]["id"] == 1
    assert json[0].get("output") is None


def test_get_test_result_by_suite_id_should_return_empty_list(
    client_with_session, suite_result, test_result
):
    url = "/api/v1/test_results/suite_result/42".format(suite_result_id=suite_result.id)

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == []


def test_get_test_result_output_should_return(client_with_session, test_result, output):
    url = "/api/v1/test_results/{}/output".format(test_result.id)

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "id": 1,
        "testResultId": 1,
        "text": "This is a long text",
    }


def test_get_test_result_output_should_404(client_with_session, test_result):
    url = "/api/v1/test_results/42/output"

    rv = client_with_session.get(url)

    assert rv.status_code == 404


def test_get_test_result_by_run_and_identifier_success(
    client_with_session, suite_result, test_result
):
    rv = client_with_session.get(
        f"/api/v1/test_results/runs/{suite_result.run_id}/{suite_result.suite_name}/{test_result.test_name}"
    )

    assert rv.status_code == 200
    assert rv.json() == {
        "unifiedTestStatus": "NOT_STARTED",
        "finishedAt": test_result.finished_at.isoformat(),
        "id": 1,
        "imageOutput": 1,
        "machineInfo": {"cores": 56, "cpuName": "cpu", "memory": 8},
        "message": "success",
        "referenceImage": 1,
        "seconds": 5.0,
        "startedAt": test_result.started_at.isoformat(),
        "suiteResultId": 1,
        "testCommand": "my_command",
        "testIdentifier": "my_suite/my_test_name",
        "testName": "my_test_name",
        "testVariables": {"testkey": "test_value"},
        "diffImage": 1,
        "comparisonSettings": None,
        "errorValue": None,
        "thumbnailFileId": None,
        "failureReason": None,
    }


def test_get_test_result_by_run_and_identifier_should_fail_invalid_run_id(
    client_with_session,
):
    rv = client_with_session.get("/api/v1/test_results/runs/10/suite_name/test_name")

    assert rv.status_code == 404


def test_get_test_result_by_run_and_identifier_should_fail_invalid_test_identifier(
    client_with_session, suite_result
):
    rv = client_with_session.get(
        f"/api/v1/test_results/runs/{suite_result.run_id}/sdrft/test_name"
    )

    assert rv.status_code == 404


def test_create_output_success(client_with_session, test_result):
    rv = client_with_session.post(
        "/api/v1/test_results/output",
        json={"testResultId": test_result.id, "text": "my text"},
    )

    assert rv.status_code == 201
    assert rv.json() == {
        "id": 1,
        "testResultId": test_result.id,
        "text": "my text",
    }


def test_create_output_failure(client_with_session, test_result):
    rv = client_with_session.post(
        "/api/v1/test_results/output", json={"testResultId": 42, "text": "my text"}
    )

    assert rv.status_code == 400
    assert rv.json() == {"testResultId": ["No test result exists for id 42."]}


def test_get_test_results_by_run_id_should_find(client_with_session, run, test_result):
    url = f"/api/v1/test_results/run/{run.id}"

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == [
        {
            "unifiedTestStatus": "NOT_STARTED",
            "id": 1,
            "name": "my_test_name",
            "testIdentifier": "my_suite/my_test_name",
            "thumbnailFileId": None,
        }
    ]


def test_get_test_results_by_run_id_should_find_with_status_filter(
    client_with_session, run, test_result
):
    url = f"/api/v1/test_results/run/{run.id}?status_filter=NOT_STARTED"

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == [
        {
            "unifiedTestStatus": "NOT_STARTED",
            "id": 1,
            "name": "my_test_name",
            "testIdentifier": "my_suite/my_test_name",
            "thumbnailFileId": None,
        }
    ]


def test_get_test_results_by_run_id_should_return_empty_list(client_with_session):
    url = f"/api/v1/test_results/run/{42}"

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == []


def test_get_test_results_by_run_id_paginated_should_find(
    client_with_session, run, test_result
):
    url = f"/api/v1/test_results/run/{run.id}?pageNumber=1&pageSize=10"

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 1,
        "entities": [
            {
                "unifiedTestStatus": "NOT_STARTED",
                "id": 1,
                "name": "my_test_name",
                "testIdentifier": "my_suite/my_test_name",
                "thumbnailFileId": None,
            }
        ],
    }


def test_get_test_results_by_run_id_paginated_should_find_with_status_filter(
    client_with_session, run, test_result
):
    url = f"/api/v1/test_results/run/{run.id}?pageNumber=1&pageSize=10&status_filter=NOT_STARTED"

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 1,
        "entities": [
            {
                "unifiedTestStatus": "NOT_STARTED",
                "id": 1,
                "name": "my_test_name",
                "testIdentifier": "my_suite/my_test_name",
                "thumbnailFileId": None,
            }
        ],
    }


def test_get_test_results_by_run_id_paginated_should_return_empty_page(
    client_with_session,
):
    url = f"/api/v1/test_results/run/{42}?pageNumber=1&pageSize=10"

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 0,
        "entities": [],
    }


def test_get_test_result_by_id(client_with_session, test_result):
    url = f"/api/v1/test_results/{test_result.id}"

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "unifiedTestStatus": "NOT_STARTED",
        "finishedAt": test_result.finished_at.isoformat(),
        "id": 1,
        "diffImage": {
            "channels": [
                {"fileId": 1, "id": 1, "imageId": 1, "name": "rgb"},
                {"fileId": 2, "id": 2, "imageId": 1, "name": "alpha"},
            ],
            "height": 1080,
            "id": 1,
            "name": "test.exr",
            "originalFileId": 1,
            "width": 1920,
        },
        "imageOutput": {
            "channels": [
                {"fileId": 1, "id": 1, "imageId": 1, "name": "rgb"},
                {"fileId": 2, "id": 2, "imageId": 1, "name": "alpha"},
            ],
            "id": 1,
            "name": "test.exr",
            "originalFileId": 1,
            "width": 1920,
            "height": 1080,
        },
        "machineInfo": {"cores": 56, "cpuName": "cpu", "memory": 8},
        "message": "success",
        "referenceImage": {
            "channels": [
                {"fileId": 1, "id": 1, "imageId": 1, "name": "rgb"},
                {"fileId": 2, "id": 2, "imageId": 1, "name": "alpha"},
            ],
            "id": 1,
            "name": "test.exr",
            "originalFileId": 1,
            "width": 1920,
            "height": 1080,
        },
        "seconds": 5.0,
        "startedAt": test_result.started_at.isoformat(),
        "suiteResultId": 1,
        "testCommand": "my_command",
        "testIdentifier": "my_suite/my_test_name",
        "testName": "my_test_name",
        "testVariables": {"testkey": "test_value"},
        "errorValue": None,
        "comparisonSettings": None,
        "thumbnailFileId": None,
    }


def test_get_test_result_by_id_no_machine_info_no_diff_image(
    client_with_session, test_result_no_machine_info
):
    url = f"/api/v1/test_results/{test_result_no_machine_info.id}"

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "unifiedTestStatus": "NOT_STARTED",
        "finishedAt": test_result_no_machine_info.finished_at.isoformat(),
        "id": 1,
        "diffImage": None,
        "imageOutput": {
            "channels": [
                {"fileId": 1, "id": 1, "imageId": 1, "name": "rgb"},
                {"fileId": 2, "id": 2, "imageId": 1, "name": "alpha"},
            ],
            "id": 1,
            "name": "test.exr",
            "originalFileId": 1,
            "width": 1920,
            "height": 1080,
        },
        "machineInfo": None,
        "message": "success",
        "referenceImage": {
            "channels": [
                {"fileId": 1, "id": 1, "imageId": 1, "name": "rgb"},
                {"fileId": 2, "id": 2, "imageId": 1, "name": "alpha"},
            ],
            "id": 1,
            "name": "test.exr",
            "originalFileId": 1,
            "width": 1920,
            "height": 1080,
        },
        "seconds": 5.0,
        "startedAt": test_result_no_machine_info.started_at.isoformat(),
        "suiteResultId": 1,
        "testCommand": "my_command",
        "testIdentifier": "my_suite/my_test_name",
        "testName": "my_test_name",
        "testVariables": {"testkey": "test_value"},
        "comparisonSettings": None,
        "errorValue": None,
        "thumbnailFileId": None,
    }


def test_get_test_results_by_run_id_should_404(client_with_session):
    url = f"/api/v1/test_results/{42}"

    rv = client_with_session.get(url)

    assert rv.status_code == 404


def test_finish_test_success(client_with_session, test_result, stored_image):
    url = "/api/v1/test_results/finish"
    data = {
        "id": test_result.id,
        "status": "SUCCESS",
        "seconds": 3,
        "message": "this is my finishing message",
        "imageOutput": stored_image.id,
        "referenceImage": stored_image.id,
        "errorValue": 1,
    }
    rv = client_with_session.post(url, json=data)

    assert rv.status_code == 200


def test_finish_test_failure(client_with_session, test_result, stored_image):
    url = "/api/v1/test_results/finish"
    data = {
        "id": test_result.id,
        "status": "SUCCESS",
        "seconds": 3,
        "message": "this is my finishing message",
        "imageOutput": 42,
        "referenceImage": stored_image.id,
        "errorValue": 1,
    }
    rv = client_with_session.post(url, json=data)

    assert rv.status_code == 400
    assert rv.json() == {"imageOutput": ["No image exists for id 42."]}


def test_should_find_by_run_id_and_test_status(client_with_session, run, test_result):
    url = f"/api/v1/test_results/run/{run.id}/test_status/NOT_STARTED"

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == ["my_suite/my_test_name"]


def test_should_not_find_by_run_id_and_test_status(
    client_with_session, run, test_result
):
    url = f"/api/v1/test_results/run/{run.id}/test_status/FAILED"

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == []


def test_invalid_test_status(client_with_session, run, test_result):
    url = f"/api/v1/test_results/run/{run.id}/test_status/dd"

    rv = client_with_session.get(url)

    assert rv.status_code == 400
    assert rv.json() == {"test_status": "Not a valid test status: dd."}


def test_start_test_success(client_with_session, test_result):
    url = "/api/v1/test_results/start"
    data = {
        "id": test_result.id,
        "machineInfo": {
            "cpuName": "test",
            "cores": 8,
            "memory": 8,
        },
    }
    rv = client_with_session.post(url, json=data)

    assert rv.status_code == 200


def test_start_test_failure(client_with_session):
    url = "/api/v1/test_results/start"
    data = {
        "id": 42,
        "machineInfo": {
            "cpuName": "test",
            "cores": 8,
            "memory": 8,
        },
    }
    rv = client_with_session.post(url, json=data)

    assert rv.status_code == 400
    assert rv.json() == {"id": ["No TestResult with id 42 exists!"]}
