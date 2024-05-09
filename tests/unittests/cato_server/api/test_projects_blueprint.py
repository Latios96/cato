API_V_PROJECTS = "/api/v1/projects"


def test_no_projects(client_with_session):
    rv = client_with_session.get(API_V_PROJECTS)

    assert rv.status_code == 200
    assert rv.json() == []


def test_get_projects(client_with_session, project):
    rv = client_with_session.get(API_V_PROJECTS)

    assert rv.status_code == 200
    assert rv.json() == [{"id": 1, "name": "test_name", "status": "ACTIVE"}]


def test_get_project_should_get(client_with_session, project):
    rv = client_with_session.get("/api/v1/projects/1")

    assert rv.status_code == 200
    assert rv.json() == {"id": 1, "name": "test_name", "status": "ACTIVE"}


def test_get_project_should_return_none(client_with_session, project):
    rv = client_with_session.get("/api/v1/projects/10")

    assert rv.status_code == 404


def test_create_project_success(client_with_session):
    rv = client_with_session.post(
        API_V_PROJECTS, json={"name": "test", "status": "ACTIVE"}
    )

    assert rv.json() == {"id": 1, "name": "test", "status": "ACTIVE"}
    assert rv.status_code == 201


def test_create_project_fail(client_with_session):
    rv = client_with_session.post(API_V_PROJECTS, json={"name": "$test"})

    assert rv.json() == {"name": ["String does not match expected pattern."]}
    assert rv.status_code == 400


def test_get_project_by_name_should_get(client_with_session, project):
    rv = client_with_session.get("/api/v1/projects/name/test_name")

    assert rv.status_code == 200
    assert rv.json() == {"id": 1, "name": "test_name", "status": "ACTIVE"}


def test_get_project_by_name_should_return_none(client_with_session, project):
    rv = client_with_session.get("/api/v1/projects/name/te")

    assert rv.status_code == 404
