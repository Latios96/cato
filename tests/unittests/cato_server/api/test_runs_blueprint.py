def test_get_run_by_project_id_should_return(client_with_session, project, run):
    url = "/api/v1/runs/project/{}".format(project.id)

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [
            {
                "id": 1,
                "projectId": 1,
                "startedAt": run.started_at.isoformat(),
                "status": "NOT_STARTED",
                "duration": 0,
                "branchName": "default",
                "runInformation": {
                    "computerName": "cray",
                    "id": 1,
                    "localUsername": "username",
                    "os": "WINDOWS",
                    "runId": 1,
                    "runInformationType": "LOCAL_COMPUTER",
                },
                "suiteCount": 0,
                "testCount": 0,
                "progress": {
                    "failedTestCount": 0,
                    "progressPercentage": 0,
                    "runningTestCount": 0,
                    "succeededTestCount": 0,
                    "waitingTestCount": 0,
                },
            }
        ],
        "pageNumber": 1,
        "pageSize": 30,
        "totalEntityCount": 1,
    }


def test_get_run_by_project_id_should_return_empty_list(client_with_session, project):
    url = "/api/v1/runs/project/{}".format(project.id)

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [],
        "pageNumber": 1,
        "pageSize": 30,
        "totalEntityCount": 0,
    }


def test_get_run_by_project_id_paged_should_return(client_with_session, project, run):
    url = "/api/v1/runs/project/{}?pageNumber=1&pageSize=10".format(project.id)

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert {
        "entities": [
            {
                "id": 1,
                "projectId": 1,
                "startedAt": run.started_at.isoformat(),
                "status": "NOT_STARTED",
                "duration": 0,
                "branchName": "default",
                "runInformation": {
                    "computerName": "cray",
                    "id": 1,
                    "localUsername": "username",
                    "os": "WINDOWS",
                    "runId": 1,
                    "runInformationType": "LOCAL_COMPUTER",
                },
                "suiteCount": 0,
                "testCount": 0,
                "progress": {
                    "failedTestCount": 0,
                    "progressPercentage": 0,
                    "runningTestCount": 0,
                    "succeededTestCount": 0,
                    "waitingTestCount": 0,
                },
            }
        ],
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 1,
    } == rv.json()


def test_get_run_by_project_id_paged_filtered_by_non_existing_branch_name_should_return_empty(
    client_with_session, project, run
):
    url = "/api/v1/runs/project/{}?pageNumber=1&pageSize=10&branches={}".format(
        project.id, "test"
    )

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [],
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 0,
    }


def test_get_run_by_project_id_paged_filtered_by_existing_branch_name_should_return(
    client_with_session, project, run
):
    url = "/api/v1/runs/project/{}?pageNumber=1&pageSize=10&branches={}".format(
        project.id, "default"
    )

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [
            {
                "id": 1,
                "projectId": 1,
                "startedAt": run.started_at.isoformat(),
                "status": "NOT_STARTED",
                "duration": 0,
                "branchName": "default",
                "runInformation": {
                    "computerName": "cray",
                    "id": 1,
                    "localUsername": "username",
                    "os": "WINDOWS",
                    "runId": 1,
                    "runInformationType": "LOCAL_COMPUTER",
                },
                "suiteCount": 0,
                "testCount": 0,
                "progress": {
                    "failedTestCount": 0,
                    "progressPercentage": 0,
                    "runningTestCount": 0,
                    "succeededTestCount": 0,
                    "waitingTestCount": 0,
                },
            }
        ],
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 1,
    }


def test_get_run_by_project_id_pages_should_return_empty_page(
    client_with_session, project
):
    url = "/api/v1/runs/project/{}?pageNumber=1&pageSize=10".format(project.id)

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [],
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 0,
    }


def test_get_run_summary(client_with_session, run, test_result):
    rv = client_with_session.get(f"/api/v1/runs/{run.id}/summary")

    assert rv.json() == {
        "id": 1,
        "projectId": 1,
        "startedAt": run.started_at.isoformat(),
        "status": "NOT_STARTED",
        "duration": 5.0,
        "branchName": "default",
        "runInformation": {
            "computerName": "cray",
            "id": 1,
            "localUsername": "username",
            "os": "WINDOWS",
            "runId": 1,
            "runInformationType": "LOCAL_COMPUTER",
        },
        "suiteCount": 1,
        "testCount": 1,
        "progress": {
            "waitingTestCount": 1,
            "failedTestCount": 0,
            "runningTestCount": 0,
            "succeededTestCount": 0,
            "progressPercentage": 0.0,
        },
    }

    assert rv.status_code == 200


def test_get_run_summary_should_error(client_with_session):
    rv = client_with_session.get("/api/v1/runs/42/summary")

    assert rv.status_code == 404


def test_run_id_exists_success(client_with_session, run):
    rv = client_with_session.get(f"/api/v1/runs/{run.id}/exists")

    assert rv.status_code == 200


def test_run_id_exists_failure(client_with_session):
    rv = client_with_session.get("/api/v1/runs/42/exists")

    assert rv.status_code == 404


def test_get_empty_branch_list(client_with_session, project):
    rv = client_with_session.get(f"/api/v1/runs/project/{project.id}/branches")

    assert rv.status_code == 200
    assert rv.json() == []


def test_get_branch_list_with_default_branch(client_with_session, project, run):
    rv = client_with_session.get(f"/api/v1/runs/project/{project.id}/branches")

    assert rv.status_code == 200
    assert rv.json() == ["default"]


CREATE_RUN_PAYLOAD_TEMPLATE = {
    "projectId": 1,
    "runBatchIdentifier": {
        "provider": "LOCAL_COMPUTER",
        "runName": "mac-os",
        "runIdentifier": "3046812908-1",
    },
    "testSuites": [
        {
            "suiteName": "my_suite",
            "suiteVariables": {},
            "tests": [
                {
                    "testName": "test_name",
                    "testIdentifier": "test/identifier",
                    "testCommand": "cmd",
                    "testVariables": {},
                    "machineInfo": {
                        "cpuName": "test",
                        "cores": 8,
                        "memory": 8,
                    },
                    "comparisonSettings": {
                        "method": "SSIM",
                        "threshold": 1,
                    },
                }
            ],
        }
    ],
}


def test_create_run_with_local_computer_run_information(
    client_with_session,
    project,
    run_batch_identifier,
    local_computer_run_information,
    object_mapper,
):
    payload = CREATE_RUN_PAYLOAD_TEMPLATE.copy()
    payload["runInformation"] = object_mapper.to_dict(local_computer_run_information)

    rv = client_with_session.post("/api/v1/runs", json=payload)

    assert rv.status_code == 201
    response_json = rv.json()
    assert response_json["runInformation"]["runInformationType"] == "LOCAL_COMPUTER"
    assert response_json["runInformation"]["runId"] == response_json["id"]


def test_create_run_with_github_actions_run_information(
    client_with_session,
    project,
    run_batch_identifier,
    github_actions_run_information,
    object_mapper,
):
    payload = CREATE_RUN_PAYLOAD_TEMPLATE.copy()
    payload["runInformation"] = object_mapper.to_dict(github_actions_run_information)

    rv = client_with_session.post("/api/v1/runs", json=payload)

    assert rv.status_code == 201
    response_json = rv.json()
    assert response_json["runInformation"]["runInformationType"] == "GITHUB_ACTIONS"
    assert response_json["runInformation"]["runId"] == response_json["id"]
