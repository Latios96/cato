import pytest

from cato_server.api.framework.abstract.request import AbstractRequest


@pytest.fixture()
def resource_for_testing(api_provider_implementation):
    ApiProvider, BaseResource = api_provider_implementation

    class ResourceForTesting(BaseResource):
        def __init__(self):
            super(ResourceForTesting, self).__init__()
            self.add_route("/hello", "GET", self.hello)
            self.add_route("/echo", "POST", self.echo)

        def hello(self):
            return {"Hello": "World"}

        def echo(self, request: AbstractRequest):
            return request.json()

    return ResourceForTesting


@pytest.fixture()
def api_provider_client_with_resource(
    api_provider_fixture, api_provider_client, resource_for_testing
):
    api_provider_fixture.register_resource(resource_for_testing(), url_prefix="")
    return api_provider_client


def test_route_without_params_should_return_json(api_provider_client_with_resource):
    response = api_provider_client_with_resource.get("/hello")

    assert response.status_code == 200
    assert response.json == {"Hello": "World"}


def test_route_without_params_should_echo_request_body_json(
    api_provider_client_with_resource,
):
    response = api_provider_client_with_resource.post("/echo", data={"Echo": "Hello"})

    assert response.status_code == 200
    assert response.json == {"Echo": "Hello"}
