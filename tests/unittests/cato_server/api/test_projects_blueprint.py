from cato_common.domain.project import ProjectStatus

API_V_PROJECTS = "/api/v1/projects"


def test_no_projects(client_with_session):
    rv = client_with_session.get(API_V_PROJECTS)

    assert rv.status_code == 200
    assert rv.json() == []


def test_get_projects(client_with_session, project):
    rv = client_with_session.get(API_V_PROJECTS)

    assert rv.status_code == 200
    assert rv.json() == [
        {"id": 1, "name": "test_name", "status": "ACTIVE", "thumbnailFileId": None}
    ]


def test_get_project_should_get(client_with_session, project):
    rv = client_with_session.get("/api/v1/projects/1")

    assert rv.status_code == 200
    assert rv.json() == {
        "id": 1,
        "name": "test_name",
        "status": "ACTIVE",
        "thumbnailFileId": None,
    }


def test_get_project_should_return_none(client_with_session, project):
    rv = client_with_session.get("/api/v1/projects/10")

    assert rv.status_code == 404


def test_create_project_success(client_with_session):
    rv = client_with_session.post(
        API_V_PROJECTS,
        json={"name": "test", "status": "ACTIVE", "thumbnailFileId": None},
    )

    assert rv.json() == {
        "id": 1,
        "name": "test",
        "status": "ACTIVE",
        "thumbnailFileId": None,
    }
    assert rv.status_code == 201


def test_create_project_fail(client_with_session):
    rv = client_with_session.post(API_V_PROJECTS, json={"name": "$test"})

    assert rv.json() == {"name": ["String does not match expected pattern."]}
    assert rv.status_code == 400


def test_get_project_by_name_should_get(client_with_session, project):
    rv = client_with_session.get("/api/v1/projects/name/test_name")

    assert rv.status_code == 200
    assert rv.json() == {
        "id": 1,
        "name": "test_name",
        "status": "ACTIVE",
        "thumbnailFileId": None,
    }


def test_get_project_by_name_should_return_none(client_with_session, project):
    rv = client_with_session.get("/api/v1/projects/name/te")

    assert rv.status_code == 404


def test_activate_project_success(
    client_with_session, project, sqlalchemy_project_repository
):
    project.status = ProjectStatus.ARCHIVED
    sqlalchemy_project_repository.save(project)

    rv = client_with_session.post(f"/api/v1/projects/{project.id}/status/active")

    assert rv.status_code == 200
    assert rv.json() == {
        "id": 1,
        "name": "test_name",
        "status": "ACTIVE",
        "thumbnailFileId": None,
    }


def test_activate_project_project_not_found(client_with_session):
    rv = client_with_session.post(f"/api/v1/projects/42/status/active")

    assert rv.status_code == 404


def test_archive_project_success(
    client_with_session, project, sqlalchemy_project_repository
):
    project.status = ProjectStatus.ACTIVE
    sqlalchemy_project_repository.save(project)

    rv = client_with_session.post(f"/api/v1/projects/{project.id}/status/archived")

    assert rv.status_code == 200
    assert rv.json() == {
        "id": 1,
        "name": "test_name",
        "status": "ARCHIVED",
        "thumbnailFileId": None,
    }


def test_archive_project_project_not_found(client_with_session):
    rv = client_with_session.post(f"/api/v1/projects/42/status/archived")

    assert rv.status_code == 404


def test_upload_project_image_success(
    client_with_session, test_resource_provider, project
):
    test_image = test_resource_provider.resource_by_name("test_image_white.jpg")
    data = {"file": ("test_image_white.jpg", open(test_image, "rb"))}
    response = client_with_session.post(
        f"/api/v1/projects/{project.id}/uploadImage", files=data
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "test_name",
        "status": "ACTIVE",
        "thumbnailFileId": 1,
    }
