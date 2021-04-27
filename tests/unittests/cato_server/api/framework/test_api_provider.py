import pytest

from cato_server.api.framework.abstract.api_provider import AbstractApiProvider
from cato_server.api.framework.abstract.api_resource import AbstractBaseResource
from cato_server.api.framework.flask_impl.flask_api_provider import FlaskApiProvider
from cato_server.api.framework.flask_impl.flask_api_resource import (
    FlaskAbstractBaseResource,
)


@pytest.fixture
def api_provider_implementation():
    return FlaskApiProvider, FlaskAbstractBaseResource


@pytest.fixture
def api_provider_fixture(api_provider_implementation):
    ApiProvider, BaseResource = api_provider_implementation
    return ApiProvider()


@pytest.fixture
def api_provider_client(api_provider_fixture: AbstractApiProvider):
    return api_provider_fixture.test_client()


@pytest.fixture()
def resource_for_testing(api_provider_implementation):
    ApiProvider, BaseResource = api_provider_implementation

    class ResourceForTesting(BaseResource):
        def __init__(self):
            super(ResourceForTesting, self).__init__()
            self.add_route("/hello", "GET", self.hello)

        def hello(self):
            return {"Hello": "World"}

    return ResourceForTesting


def test_register_resource(
    api_provider_fixture,
    api_provider_client,
    api_provider_implementation,
    resource_for_testing,
):
    api_provider_fixture.register_resource(resource_for_testing(), url_prefix="")

    response = api_provider_client.get("/hello")
    assert response.json == {"Hello": "World"}
    assert response.status_code == 200


def test_register_resource_invalid_url_prefix(
    api_provider_fixture,
    api_provider_client,
    api_provider_implementation,
    resource_for_testing,
):
    with pytest.raises(ValueError):
        api_provider_fixture.register_resource(resource_for_testing(), url_prefix="/")


def test_register_resource_with_url_prefix(
    api_provider_fixture, api_provider_client, api_provider_implementation
):
    ApiProvider, BaseResource = api_provider_implementation

    class ResourceForTesting(BaseResource):
        def __init__(self):
            super(ResourceForTesting, self).__init__()
            self.add_route("/hello", "GET", self.hello)

        def hello(self):
            return {"Hello": "World"}

    api_provider_fixture.register_resource(ResourceForTesting(), url_prefix="/api/v1")

    response = api_provider_client.get("/api/v1/hello")
    assert response.json == {"Hello": "World"}
    assert response.status_code == 200
