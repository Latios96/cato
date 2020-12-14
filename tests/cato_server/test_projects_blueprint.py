API_V_PROJECTS = "/api/v1/projects"


def test_no_projects(client):
    rv = client.get(API_V_PROJECTS)

    assert rv.status_code == 200
    assert rv.get_json() == []


def test_get_projects(client, project):
    rv = client.get(API_V_PROJECTS)

    assert rv.status_code == 200
    assert rv.get_json() == [{"id": 1, "name": "test_name"}]


def test_get_project_should_get(client, project):
    rv = client.get("/api/v1/projects/1")

    assert rv.status_code == 200
    assert rv.get_json() == {"id": 1, "name": "test_name"}


def test_get_project_should_return_none(client, project):
    rv = client.get("/api/v1/projects/10")

    assert rv.status_code == 404


def test_create_project_success(client):
    rv = client.post(API_V_PROJECTS, json={"name": "test"})

    assert rv.get_json() == {"id": 1, "name": "test"}
    assert rv.status_code == 201


def test_create_project_fail(client):
    rv = client.post(API_V_PROJECTS, json={"name": "$test"})

    assert rv.get_json() == {"name": ["String does not match expected pattern."]}
    assert rv.status_code == 400


def test_get_project_by_name_should_get(client, project):
    rv = client.get("/api/v1/projects/name/test_name")

    assert rv.status_code == 200
    assert rv.get_json() == {"id": 1, "name": "test_name"}


def test_get_project_by_name_should_return_none(client, project):
    rv = client.get("/api/v1/projects/name/te")

    assert rv.status_code == 404
