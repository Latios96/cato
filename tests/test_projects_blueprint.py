import pytest

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


@pytest.mark.parametrize(
    "project_name",
    [
        "my_project_name",
        "my-project_name",
        "my-project_name222",
        "22",
        "My-Project-Name",
    ],
)
def test_create_project(client, project_name):
    rv = client.post(API_V_PROJECTS, json={"name": project_name})

    assert rv.get_json() == {"id": 1, "name": project_name}
    assert rv.status_code == 201


def test_create_project_same_name_should_fail(client):
    client.post(API_V_PROJECTS, json={"name": "test"})
    rv = client.post(API_V_PROJECTS, json={"name": "test"})

    assert rv.get_json() == {"name": ['Project with name "test" already exists!']}
    assert rv.status_code == 400


def test_create_project_no_name(client):
    rv = client.post(API_V_PROJECTS, json={"xfcgvy": "my_project_name"})

    assert rv.status_code == 400
    assert rv.get_json() == {
        "name": ["Missing data for required field."],
        "xfcgvy": ["Unknown field."],
    }


@pytest.mark.parametrize(
    "invalid_project_name,error_messages",
    [
        ("my invalid name", ["String does not match expected pattern."]),
        ("myinvalid%name", ["String does not match expected pattern."]),
        ("myinvalid$name", ["String does not match expected pattern."]),
        ("myinvalid§*+*name", ["String does not match expected pattern."]),
        ("myinvalid/name", ["String does not match expected pattern."]),
        ("myinvalid\\name", ["String does not match expected pattern."]),
        ("my invalid&name", ["String does not match expected pattern."]),
        ("my invalid name", ["String does not match expected pattern."]),
        (
            "",
            [
                "Shorter than minimum length 1.",
                "String does not match expected pattern.",
            ],
        ),
    ],
)
def test_create_project_invalid_name(client, invalid_project_name, error_messages):
    rv = client.post(API_V_PROJECTS, json={"name": invalid_project_name})

    assert rv.status_code == 400
    assert rv.get_json() == {
        "name": error_messages,
    }


def test_get_project_by_name_should_get(client, project):
    rv = client.get("/api/v1/projects/name/test_name")

    assert rv.status_code == 200
    assert rv.get_json() == {"id": 1, "name": "test_name"}


def test_get_project_by_name_should_return_none(client, project):
    rv = client.get("/api/v1/projects/name/te")

    assert rv.status_code == 404
