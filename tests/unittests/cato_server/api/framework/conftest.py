import pytest

from cato_server.api.framework.abstract.api_provider import AbstractApiProvider
from cato_server.api.framework.fast_api_impl.fast_api_api_provider import (
    FastApiApiProvider,
)
from cato_server.api.framework.fast_api_impl.fast_api_api_resource import (
    FastApiAbstractBaseResource,
)
from cato_server.api.framework.flask_impl.flask_api_provider import FlaskApiProvider
from cato_server.api.framework.flask_impl.flask_api_resource import (
    FlaskAbstractBaseResource,
)


def pytest_generate_tests(metafunc):
    has_api_provider_fixture = "api_provider_implementation" in metafunc.fixturenames
    if has_api_provider_fixture:
        metafunc.parametrize(
            "api_provider_implementation",
            [
                (FlaskApiProvider, FlaskAbstractBaseResource),
                (FastApiApiProvider, FastApiAbstractBaseResource),
            ],
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
