import datetime


def test_get_run_by_project_id_should_return(client, project, run):
    url = "/api/v1/runs/project/{}".format(project.id)

    rv = client.get(url)

    assert rv.status_code == 200
    json = rv.get_json()
    assert len(json) == 1
    assert json[0]["id"] == 1
    assert json[0]["project_id"] == 1


def test_get_run_by_project_id_should_return_empty_list(client, project):
    url = "/api/v1/runs/project/{}".format(project.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.get_json() == []


def test_get_run_by_project_id_paged_should_return(client, project, run):
    url = "/api/v1/runs/project/{}?page_number=1&page_size=10".format(project.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.get_json() == {
        "entities": [
            {
                "id": 1,
                "project_id": 1,
                "started_at": run.started_at.isoformat(),
                "status": "NOT_STARTED",
            }
        ],
        "page_number": 1,
        "page_size": 10,
        "total_entity_count": 1,
    }


def test_get_run_by_project_id_pages_should_return_empty_page(client, project):
    url = "/api/v1/runs/project/{}?page_number=1&page_size=10".format(project.id)

    rv = client.get(url)

    assert rv.status_code == 200
    assert rv.get_json() == {
        "entities": [],
        "page_number": 1,
        "page_size": 10,
        "total_entity_count": 0,
    }


def test_create_run_success(client, project):
    started_at = datetime.datetime.now()

    rv = client.post(
        "/api/v1/runs",
        json={"project_id": project.id, "started_at": started_at.isoformat()},
    )

    assert rv.get_json() == {
        "id": 1,
        "project_id": project.id,
        "started_at": started_at.isoformat(),
    }
    assert rv.status_code == 201


def test_create_run_failure(client):
    started_at = datetime.datetime.now()

    rv = client.post(
        "/api/v1/runs", json={"project_id": 2, "started_at": started_at.isoformat()}
    )

    assert rv.status_code == 400
    assert rv.get_json() == {"project_id": ["No project with id 2 exists!"]}


def test_get_status(client, run, test_result):
    rv = client.get(f"/api/v1/runs/{run.id}/status")

    assert rv.status_code == 200
    assert rv.get_json() == {"status": "NOT_STARTED"}


def test_get_status_404(client, run):
    rv = client.get(f"/api/v1/runs/{run.id}/status")

    assert rv.status_code == 404


def test_get_run_summary(client, run, test_result):
    rv = client.get(f"/api/v1/runs/{run.id}/summary")

    assert rv.status_code == 200
    assert rv.get_json() == {
        "duration": 5.0,
        "failed_test_count": 0,
        "run": {
            "id": 1,
            "project_id": 1,
            "started_at": run.started_at.isoformat(),
            "status": "NOT_STARTED",
        },
        "suite_count": 1,
        "test_count": 1,
    }


def test_get_run_summary_shold_error(client):
    rv = client.get("/api/v1/runs/42/summary")

    assert rv.status_code == 404
