from unittest import mock

import pytest

from cato_api_client.http_template import (
    HttpTemplate,
    HttpTemplateException,
    InternalServerError,
    Unauthorized,
)
from cato_common.domain.project import Project


class Response:
    def __init__(self, status_code, json_value):
        self.status_code = status_code
        self._json_value = json_value

    def json(self):
        return self._json_value


@mock.patch("requests.Session.get")
def test_get_for_entity_success(mock_requests_get, object_mapper):
    mock_requests_get.return_value = Response(200, {"id": 1, "name": "test-project"})
    http_template = HttpTemplate(object_mapper)

    response = http_template.get_for_entity("/ap1/v1/projects/test-project", Project)

    assert response.status_code() == 200
    assert response.get_entity() == Project(id=1, name="test-project")


@mock.patch("requests.Session.get")
def test_get_many_for_entity_success(mock_requests_get, object_mapper):
    mock_requests_get.return_value = Response(
        200, [{"id": 1, "name": "test-project"}, {"id": 2, "name": "test-project"}]
    )
    http_template = HttpTemplate(object_mapper)

    response = http_template.get_for_entity("/ap1/v1/projects/test-project", Project)

    assert response.status_code() == 200
    assert response.get_entities() == [
        Project(id=1, name="test-project"),
        Project(id=2, name="test-project"),
    ]


@mock.patch("requests.Session.get")
def test_get_for_entity_404(mock_requests_get, object_mapper):
    mock_requests_get.return_value = Response(404, None)
    http_template = HttpTemplate(object_mapper)

    response = http_template.get_for_entity("/ap1/v1/projects/test-project", Project)

    assert response.status_code() == 404
    with pytest.raises(ValueError):
        response.get_entity()


@mock.patch("requests.Session.get")
def test_get_for_entity_500(mock_requests_get, object_mapper):
    mock_requests_get.return_value = Response(500, None)
    http_template = HttpTemplate(object_mapper)

    with pytest.raises(InternalServerError):
        http_template.get_for_entity("/ap1/v1/projects/test-project", Project)


@mock.patch("requests.Session.get")
def test_get_for_entity_401(mock_requests_get, object_mapper):
    mock_requests_get.return_value = Response(401, None)
    http_template = HttpTemplate(object_mapper)

    with pytest.raises(Unauthorized):
        http_template.get_for_entity("/ap1/v1/projects/test-project", Project)


@mock.patch("requests.Session.post")
def test_post_for_entity_success(mock_requests_post, object_mapper):
    mock_requests_post.return_value = Response(200, {"id": 2, "name": "test-project"})
    http_template = HttpTemplate(object_mapper)

    response = http_template.post_for_entity(
        "/ap1/v1/projects/test-project", Project(id=1, name="test"), Project
    )

    assert response.status_code() == 200
    assert response.get_entity() == Project(id=2, name="test-project")


@mock.patch("requests.Session.post")
def test_post_for_entity_404(mock_requests_post, object_mapper):
    mock_requests_post.return_value = Response(404, None)
    http_template = HttpTemplate(object_mapper)

    response = http_template.post_for_entity(
        "/ap1/v1/projects/test-project",
        Project(id=1, name="test"),
        Project,
    )

    assert response.status_code() == 404
    with pytest.raises(ValueError):
        response.get_entity()


@mock.patch("requests.Session.patch")
def test_patch_for_entity_success(mock_requests_post, object_mapper):
    mock_requests_post.return_value = Response(200, {"id": 2, "name": "test-project"})
    http_template = HttpTemplate(object_mapper)

    response = http_template.patch_for_entity(
        "/ap1/v1/projects/test-project", Project(id=1, name="test"), Project
    )

    assert response.status_code() == 200
    assert response.get_entity() == Project(id=2, name="test-project")


@mock.patch("requests.Session.patch")
def test_patch_for_entity_404(mock_requests_post, object_mapper):
    mock_requests_post.return_value = Response(404, None)
    http_template = HttpTemplate(object_mapper)

    response = http_template.patch_for_entity(
        "/ap1/v1/projects/test-project", Project(id=1, name="test"), Project
    )

    assert response.status_code() == 404
    with pytest.raises(ValueError):
        response.get_entity()
