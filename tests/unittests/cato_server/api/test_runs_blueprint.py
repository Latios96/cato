def test_get_run_by_project_id_should_return(client, project, run):
    url = "/api/v1/runs/project/{}".format(project.id)

    rv = client.get(url)

    assert rv.status_code == 200
    json = rv.json()
    assert len(json) == 1
    assert json[0]["id"] == 1
    assert json[0]["projectId"] == 1


def test_get_run_by_project_id_should_return_empty_list(client, project):
    url = "/api/v1/runs/project/{}".format(project.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == []


def test_get_run_by_project_id_paged_should_return(client, project, run):
    url = "/api/v1/runs/project/{}?pageNumber=1&pageSize=10".format(project.id)

    rv = client.get(url)

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
            }
        ],
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 1,
    }


def test_get_run_by_project_id_paged_filtered_by_non_existing_branch_name_should_return_empty(
    client, project, run
):
    url = "/api/v1/runs/project/{}?pageNumber=1&pageSize=10&branches={}".format(
        project.id, "test"
    )

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [],
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 0,
    }


def test_get_run_by_project_id_paged_filtered_by_existing_branch_name_should_return(
    client, project, run
):
    url = "/api/v1/runs/project/{}?pageNumber=1&pageSize=10&branches={}".format(
        project.id, "default"
    )

    rv = client.get(url)

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
            }
        ],
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 1,
    }


def test_get_run_by_project_id_pages_should_return_empty_page(client, project):
    url = "/api/v1/runs/project/{}?pageNumber=1&pageSize=10".format(project.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "entities": [],
        "pageNumber": 1,
        "pageSize": 10,
        "totalEntityCount": 0,
    }


def test_get_status(client, run, test_result):
    rv = client.get(f"/api/v1/runs/{run.id}/status")

    assert rv.status_code == 200
    assert rv.json() == {"status": "NOT_STARTED"}


def test_get_status_404(client, run):
    rv = client.get(f"/api/v1/runs/{run.id}/status")

    assert rv.status_code == 404


def test_get_run_summary(client, run, test_result):
    rv = client.get(f"/api/v1/runs/{run.id}/summary")

    assert rv.json() == {
        "waitingTestCount": 1,
        "failedTestCount": 0,
        "runningTestCount": 0,
        "succeededTestCount": 0,
        "run": {
            "id": 1,
            "projectId": 1,
            "startedAt": run.started_at.isoformat(),
            "status": "NOT_STARTED",
            "duration": 5.0,
            "branchName": "default",
        },
        "suiteCount": 1,
        "testCount": 1,
    }
    assert rv.status_code == 200


def test_get_run_summary_should_error(client):
    rv = client.get("/api/v1/runs/42/summary")

    assert rv.status_code == 404


def test_run_id_exists_success(client, run):
    rv = client.get(f"/api/v1/runs/{run.id}/exists")

    assert rv.status_code == 200


def test_run_id_exists_failure(client):
    rv = client.get("/api/v1/runs/42/exists")

    assert rv.status_code == 404


def test_get_empty_branch_list(client, project):
    rv = client.get(f"/api/v1/runs/project/{project.id}/branches")

    assert rv.status_code == 200
    assert rv.json() == []


def test_get_branch_list_with_default_branch(client, project, run):
    rv = client.get(f"/api/v1/runs/project/{project.id}/branches")

    assert rv.status_code == 200
    assert rv.json() == ["default"]
