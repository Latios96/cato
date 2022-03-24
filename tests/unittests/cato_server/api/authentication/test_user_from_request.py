from dataclasses import dataclass

import pytest

from cato_server.api.authentication.user_from_request import UserFromRequest
from cato_server.authentication.api_token_signer import (
    ApiTokenSigner,
    InvalidApiTokenException,
)
from cato_server.authentication.session_backend import SessionBackend
from cato_server.domain.auth.session_id import SessionId
from cato_server.storage.abstract.auth_user_repository import AuthUserRepository
from tests.utils import mock_safe


@pytest.fixture
def user_from_request_fixture():
    @dataclass
    class UserFromRequestFixture:
        mock_session_backend: SessionBackend
        mock_auth_user_repository: AuthUserRepository
        mock_api_token_signer: ApiTokenSigner
        user_from_request: UserFromRequest

    mock_session_backend = mock_safe(SessionBackend)
    mock_auth_user_repository = mock_safe(AuthUserRepository)
    mock_api_token_signer = mock_safe(ApiTokenSigner)
    user_from_request = UserFromRequest(
        mock_session_backend, mock_auth_user_repository, mock_api_token_signer
    )

    return UserFromRequestFixture(
        mock_session_backend,
        mock_auth_user_repository,
        mock_api_token_signer,
        user_from_request,
    )


def test_should_return_session_from_request_if_found(
    request_factory, user_from_request_fixture, fixed_http_session
):
    user_from_request_fixture.mock_session_backend.get_session.return_value = (
        fixed_http_session
    )
    request = request_factory("/test", session_dict={"session_id": "my_session_id"})

    session = user_from_request_fixture.user_from_request.session_from_request(request)

    assert session == fixed_http_session
    user_from_request_fixture.mock_session_backend.get_session.assert_called_with(
        SessionId("my_session_id")
    )


def test_should_not_return_session_from_request_if_no_valid_session_found(
    request_factory, user_from_request_fixture
):
    user_from_request_fixture.mock_session_backend.get_session.return_value = None
    request = request_factory("/test", session_dict={"session_id": "my_session_id"})

    session = user_from_request_fixture.user_from_request.session_from_request(request)

    assert session is None
    user_from_request_fixture.mock_session_backend.get_session.assert_called_with(
        SessionId("my_session_id")
    )


def test_should_not_return_session_from_request_if_session_cookie_not_present(
    request_factory, user_from_request_fixture
):
    request = request_factory("/test")

    session = user_from_request_fixture.user_from_request.session_from_request(request)

    assert session is None
    user_from_request_fixture.mock_session_backend.get_session.assert_not_called()


def test_should_return_user_for_session_from_request_if_found(
    request_factory, user_from_request_fixture, fixed_http_session, auth_user
):
    user_from_request_fixture.mock_session_backend.get_session.return_value = (
        fixed_http_session
    )
    user_from_request_fixture.mock_auth_user_repository.find_by_id.return_value = (
        auth_user
    )
    request = request_factory("/test", session_dict={"session_id": "my_session_id"})

    user_from_request = user_from_request_fixture.user_from_request.user_from_request(
        request
    )

    assert user_from_request == auth_user
    user_from_request_fixture.mock_session_backend.get_session.assert_called_with(
        SessionId("my_session_id")
    )
    user_from_request_fixture.mock_auth_user_repository.find_by_id.assert_called_with(1)


def test_should_not_return_user_for_session_from_request_if_no_valid_session_found(
    request_factory, user_from_request_fixture
):
    user_from_request_fixture.mock_session_backend.get_session.return_value = None
    request = request_factory("/test", session_dict={"session_id": "my_session_id"})

    user_from_request = user_from_request_fixture.user_from_request.user_from_request(
        request
    )

    assert user_from_request is None
    user_from_request_fixture.mock_session_backend.get_session.assert_called_with(
        SessionId("my_session_id")
    )
    user_from_request_fixture.mock_auth_user_repository.find_by_id.assert_not_called()


def test_should_return_api_token_from_request_if_found(
    request_factory, user_from_request_fixture, fixed_api_token_str, fixed_api_token
):
    user_from_request_fixture.mock_api_token_signer.unsign.return_value = (
        fixed_api_token
    )
    request = request_factory(
        "/test", auth_header=bytes(fixed_api_token_str.to_bearer())
    )

    api_token = user_from_request_fixture.user_from_request.api_token_from_request(
        request
    )

    assert api_token == fixed_api_token
    user_from_request_fixture.mock_api_token_signer.unsign.assert_called_with(
        fixed_api_token_str
    )


def test_should_not_return_api_token_from_request_if_not_found(
    request_factory, user_from_request_fixture
):
    user_from_request_fixture.mock_session_backend.get_session.return_value = None
    request = request_factory("/test")

    api_token = user_from_request_fixture.user_from_request.api_token_from_request(
        request
    )

    assert api_token is None
    user_from_request_fixture.mock_api_token_signer.unsign.assert_not_called()


def test_should_not_return_api_token_from_request_if_invalid(
    request_factory, user_from_request_fixture, fixed_api_token_str, fixed_api_token
):
    user_from_request_fixture.mock_api_token_signer.unsign.side_effect = (
        InvalidApiTokenException
    )
    request = request_factory(
        "/test", auth_header=bytes(fixed_api_token_str.to_bearer())
    )

    api_token = user_from_request_fixture.user_from_request.api_token_from_request(
        request
    )

    assert api_token is None
    user_from_request_fixture.mock_api_token_signer.unsign.assert_called_with(
        fixed_api_token_str
    )
