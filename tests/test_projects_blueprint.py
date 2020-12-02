import pytest

from cato.storage.sqlalchemy.sqlalchemy_config import SqlAlchemyConfig
from cato_server.__main__ import create_app

API_V_PROJECTS = "/api/v1/projects"


class SqlAlchemyTestConfig(SqlAlchemyConfig):
    def __init__(self, session_maker, file_storage_path):
        self.session_maker = session_maker
        self._file_storage_path = file_storage_path

    def get_session_maker(self):
        return self.session_maker

    def get_file_storage_path(self):
        return self._file_storage_path


@pytest.fixture
def client(sessionmaker_fixture, tmp_path):
    config = SqlAlchemyTestConfig(sessionmaker_fixture, str(tmp_path))
    app = create_app(config)

    with app.test_client() as client:
        yield client


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
