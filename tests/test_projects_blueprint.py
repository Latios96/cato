import pytest

from cato.storage.sqlalchemy.sqlalchemy_config import SqlAlchemyConfig
from cato_server.__main__ import create_app


class SqlAlchemyTestConfig(SqlAlchemyConfig):
    def __init__(self, session_maker):
        self.session_maker = session_maker

    def get_session_maker(self):
        return self.session_maker


@pytest.fixture
def client(sessionmaker_fixture):
    config = SqlAlchemyTestConfig(sessionmaker_fixture)
    app = create_app(config)

    with app.test_client() as client:
        yield client


def test_no_projects(client):
    rv = client.get("/api/v1/projects")

    assert rv.status_code == 200
    assert rv.get_json() == []


def test_get_projects(client, project):
    rv = client.get("/api/v1/projects")

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
    rv = client.post("/api/v1/projects", data={"name": "my_project_name"})

    assert rv.status_code == 200
    assert rv.get_json() == {"id": 1, "name": "my_project_name"}


def test_create_project_no_name(client):
    rv = client.post("/api/v1/projects", data={"xfcgvy": "my_project_name"})

    assert rv.status_code == 400
    assert rv.get_json() == {
        "name": ["Missing data for required field."],
        "xfcgvy": ["Unknown field."],
    }
