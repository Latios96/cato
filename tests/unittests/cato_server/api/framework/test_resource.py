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
            self.add_route("/echo/<int:id>", "GET", self.echo_id)
            self.add_route("/echo_all/<int:id>/test/<test>", "GET", self.echo_all)

        def hello(self):
            return {"Hello": "World"}

        def echo(self, request: AbstractRequest):
            return request.json()

        def echo_id(self, id):
            return {"Hello": id}

        def echo_all(self, *args, **kwargs):
            return {"Hello": kwargs}

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


def test_route_with_params_should_echo(api_provider_client_with_resource):
    response = api_provider_client_with_resource.get("/echo/1")

    assert response.status_code == 200
    assert response.json == {"Hello": 1}


def test_route_with_many_params_should_echo(api_provider_client_with_resource):
    response = api_provider_client_with_resource.get(
        "/echo_all/1/test/d91a632a-75f7-4e79-ae77-e6f33010c672"
    )

    assert response.status_code == 200
    assert response.json == {
        "Hello": {"id": 1, "test": "d91a632a-75f7-4e79-ae77-e6f33010c672"}
    }
