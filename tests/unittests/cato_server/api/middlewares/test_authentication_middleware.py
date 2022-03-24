from dataclasses import dataclass
from typing import Callable, Awaitable

import pytest
from asyncmock import AsyncMock
from starlette.requests import Request
from starlette.responses import Response

from cato_server.api.authentication.user_from_request import UserFromRequest
from cato_server.api.middlewares.authentication_middleware import (
    AuthenticationMiddleware,
)
from cato_server.authentication.api_token_signer import ApiTokenSigner
from tests.utils import mock_safe

UNPROTECTED_ROUTES = ["/", "/index.html", "/static", "/login", "/auth"]
PROTECTED_ROUTES = ["/api/v1/projects"]


@pytest.fixture
def authentication_middleware_fixture():
    @dataclass
    class AuthenticationMiddlewareFixture:
        api_token_signer: ApiTokenSigner
        user_from_request: UserFromRequest
        mock_call_next: Callable[[Request], Awaitable[Response]]
        authentication_middleware: AuthenticationMiddleware

    api_token_signer = mock_safe(ApiTokenSigner)
    user_from_request = mock_safe(UserFromRequest)
    user_from_request.api_token_from_request.return_value = None
    user_from_request.session_from_request.return_value = None
    mock_call_next = AsyncMock(return_value=Response(status_code=200))
    authentication_middleware = AuthenticationMiddleware(
        api_token_signer, user_from_request
    )
    return AuthenticationMiddlewareFixture(
        api_token_signer, user_from_request, mock_call_next, authentication_middleware
    )


@pytest.mark.parametrize("unprotected_route", UNPROTECTED_ROUTES)
async def test_unprotected_route_should_work_for_no_session_or_bearer(
    authentication_middleware_fixture, request_factory, unprotected_route
):
    request = request_factory(unprotected_route)

    response = await authentication_middleware_fixture.authentication_middleware(
        request, authentication_middleware_fixture.mock_call_next
    )

    assert response.status_code == 200


@pytest.mark.parametrize("unprotected_route", UNPROTECTED_ROUTES)
async def test_unprotected_route_should_work_for_valid_bearer(
    authentication_middleware_fixture,
    request_factory,
    unprotected_route,
    fixed_api_token,
):
    authentication_middleware_fixture.user_from_request.api_token_from_request.return_value = (
        fixed_api_token
    )
    request = request_factory(unprotected_route)

    response = await authentication_middleware_fixture.authentication_middleware(
        request, authentication_middleware_fixture.mock_call_next
    )

    assert response.status_code == 200


@pytest.mark.parametrize("unprotected_route", UNPROTECTED_ROUTES)
async def test_unprotected_route_should_work_for_valid_session(
    authentication_middleware_fixture,
    request_factory,
    unprotected_route,
    fixed_http_session,
):
    authentication_middleware_fixture.user_from_request.session_from_request.return_value = (
        fixed_http_session
    )
    request = request_factory(unprotected_route)

    response = await authentication_middleware_fixture.authentication_middleware(
        request, authentication_middleware_fixture.mock_call_next
    )

    assert response.status_code == 200


@pytest.mark.parametrize("protected_route", PROTECTED_ROUTES)
async def test_protected_route_should_not_work_for_no_session_or_bearer(
    authentication_middleware_fixture, request_factory, protected_route
):
    request = request_factory(protected_route)

    response = await authentication_middleware_fixture.authentication_middleware(
        request, authentication_middleware_fixture.mock_call_next
    )

    assert response.status_code == 401


@pytest.mark.parametrize("protected_route", PROTECTED_ROUTES)
async def test_protected_route_should_work_for_valid_bearer(
    authentication_middleware_fixture, request_factory, protected_route, fixed_api_token
):
    authentication_middleware_fixture.user_from_request.api_token_from_request.return_value = (
        fixed_api_token
    )
    request = request_factory(protected_route)

    response = await authentication_middleware_fixture.authentication_middleware(
        request, authentication_middleware_fixture.mock_call_next
    )

    assert response.status_code == 200


@pytest.mark.parametrize("protected_route", PROTECTED_ROUTES)
async def test_protected_route_should_work_for_valid_session(
    authentication_middleware_fixture,
    request_factory,
    protected_route,
    fixed_http_session,
):
    authentication_middleware_fixture.user_from_request.session_from_request.return_value = (
        fixed_http_session
    )
    request = request_factory(protected_route)

    response = await authentication_middleware_fixture.authentication_middleware(
        request, authentication_middleware_fixture.mock_call_next
    )

    assert response.status_code == 200
