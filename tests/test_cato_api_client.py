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

    def _get_json(self, reponse):
        return reponse.get_json()


def test_get_project_by_name_should_get_project(
    app_and_config_fixture, client, project
):
    app, config = app_and_config_fixture
    api_client = CatoApiTestClient(f"http://localhost:{config.port}", client)

    project = api_client.get_project_by_name("test_name")

    assert project == Project(1, "test_name")


def test_get_project_by_name_should_get_none(app_and_config_fixture, client, project):
    app, config = app_and_config_fixture
    api_client = CatoApiTestClient(f"http://localhost:{config.port}", client)

    project = api_client.get_project_by_name("ysdf")

    assert project is None
