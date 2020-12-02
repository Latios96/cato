import pytest
from requests.models import Response

from cato.domain.project import Project
from cato_api_client.cato_api_client import CatoApiClient


class CatoApiTestClient(CatoApiClient):
    def __init__(self, url, client):
        super(CatoApiTestClient, self).__init__(url)
        self._client = client

    def _get(self, url: str) -> Response:
        get = self._client.get(url.replace(self._url, ""))
        return get

    def _post(self, url, params):
        return self._client.post(url.replace(self._url, ""), data=params)

    def _get_json(self, reponse):
        return reponse.get_json()


@pytest.fixture
def cato_api_client(app_and_config_fixture, client):
    pp, config = app_and_config_fixture
    api_client = CatoApiTestClient(f"http://localhost:{config.port}", client)
    return api_client


def test_get_project_by_name_should_get_project(cato_api_client, project):
    project = cato_api_client.get_project_by_name("test_name")

    assert project == Project(1, "test_name")


def test_get_project_by_name_should_get_none(cato_api_client):
    project = cato_api_client.get_project_by_name("ysdf")

    assert project is None


def test_create_project_should_create_project(cato_api_client):
    project = cato_api_client.create_project("my_project")

    assert project == Project(id=1, name="my_project")


def test_create_project_should_not_create_invalid_name(cato_api_client):
    with pytest.raises(ValueError):
        cato_api_client.create_project("my project")
