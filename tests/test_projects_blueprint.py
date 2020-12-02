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


def test_create_project(client):
    rv = client.post(API_V_PROJECTS, data={"name": "my_project_name"})

    assert rv.status_code == 200
    assert rv.get_json() == {"id": 1, "name": "my_project_name"}


def test_create_project_no_name(client):
    rv = client.post(API_V_PROJECTS, data={"xfcgvy": "my_project_name"})

    assert rv.status_code == 400
    assert rv.get_json() == {
        "name": ["Missing data for required field."],
        "xfcgvy": ["Unknown field."],
    }


def test_get_project_by_name_should_get(client, project):
    rv = client.get("/api/v1/projects/name/test_name")

    assert rv.status_code == 200
    assert rv.get_json() == {"id": 1, "name": "test_name"}


def test_get_project_by_name_should_return_none(client, project):
    rv = client.get("/api/v1/projects/name/te")

    assert rv.status_code == 404
