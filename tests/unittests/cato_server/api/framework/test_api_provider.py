import pytest


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


class TestRegisterResource:
    def test_register_resource(
        self,
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
        self,
        api_provider_fixture,
        api_provider_client,
        api_provider_implementation,
        resource_for_testing,
    ):
        with pytest.raises(ValueError):
            api_provider_fixture.register_resource(
                resource_for_testing(), url_prefix="/"
            )

    def test_register_resource_with_url_prefix(
        self, api_provider_fixture, api_provider_client, api_provider_implementation
    ):
        ApiProvider, BaseResource = api_provider_implementation

        class ResourceForTesting(BaseResource):
            def __init__(self):
                super(ResourceForTesting, self).__init__()
                self.add_route("/hello", "GET", self.hello)

            def hello(self):
                return {"Hello": "World"}

        api_provider_fixture.register_resource(
            ResourceForTesting(), url_prefix="/api/v1"
        )

        response = api_provider_client.get("/api/v1/hello")
        assert response.json == {"Hello": "World"}
        assert response.status_code == 200
