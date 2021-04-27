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
