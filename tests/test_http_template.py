from typing import Dict
from unittest import mock

import pytest

from cato.domain.project import Project
from cato.mappers.abstract_class_mapper import AbstractClassMapper
from cato_api_client.http_template import HttpTemplate, HttpTemplateException


class Response:
    def __init__(self, status_code, json_value):
        self.status_code = status_code
        self._json_value = json_value

    def json(self):
        return self._json_value


class ProjectMapper(AbstractClassMapper[Project]):
    def map_from_dict(self, json_data: Dict) -> Project:
        return Project(json_data["id"], json_data["name"])

    def map_to_dict(self, project: Project) -> Dict:
        return {"id": project.id, "name": project.name}


@mock.patch("requests.get")
def test_get_for_entity_success(mock_requests_get):
    mock_requests_get.return_value = Response(200, {"id": 1, "name": "test-project"})
    http_template = HttpTemplate()

    response = http_template.get_for_entity(
        "/ap1/v1/projects/test-project", ProjectMapper()
    )

    assert response.status_code() == 200
    assert response.get_entity() == Project(id=1, name="test-project")


@mock.patch("requests.get")
def test_get_for_entity_404(mock_requests_get):
    mock_requests_get.return_value = Response(404, None)
    http_template = HttpTemplate()

    response = http_template.get_for_entity(
        "/ap1/v1/projects/test-project", ProjectMapper()
    )

    assert response.status_code() == 404
    with pytest.raises(TypeError):
        response.get_entity()


@mock.patch("requests.get")
def test_get_for_entity_500(mock_requests_get):
    mock_requests_get.return_value = Response(500, None)
    http_template = HttpTemplate()

    with pytest.raises(HttpTemplateException):
        http_template.get_for_entity("/ap1/v1/projects/test-project", ProjectMapper())


@mock.patch("requests.post")
def test_post_for_entity_success(mock_requests_post):
    mock_requests_post.return_value = Response(200, {"id": 2, "name": "test-project"})
    http_template = HttpTemplate()

    response = http_template.post_for_entity(
        "/ap1/v1/projects/test-project",
        Project(id=1, name="test"),
        ProjectMapper(),
        ProjectMapper(),
    )

    assert response.status_code() == 200
    assert response.get_entity() == Project(id=2, name="test-project")


@mock.patch("requests.post")
def test_post_for_entity_404(mock_requests_post):
    mock_requests_post.return_value = Response(404, None)
    http_template = HttpTemplate()

    response = http_template.post_for_entity(
        "/ap1/v1/projects/test-project",
        Project(id=1, name="test"),
        ProjectMapper(),
        ProjectMapper(),
    )

    assert response.status_code() == 404
    with pytest.raises(TypeError):
        response.get_entity()
