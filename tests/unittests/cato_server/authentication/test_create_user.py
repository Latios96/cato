from unittest import mock

import pytest

from cato_server.authentication.create_user import (
    CreateUserData,
    CreateUser,
    UsernameAlreadyExistsException,
    EmailAlreadyExistsException,
)
from cato_server.authentication.crypto_context import CryptoContext
from cato_server.domain.auth.auth_user import AuthUser
from cato_server.domain.auth.email import Email
from cato_server.domain.auth.username import Username
from cato_server.storage.abstract.auth_user_repository import (
    AuthUserRepository,
)
from tests.utils import mock_safe

USERNAME = Username("username")
FULLNAME = Username("User Username")
EMAIL = Email("foo@bar.com")


def mocked_safe(auth_user):
    auth_user.id = 1
    return auth_user


@pytest.fixture
def create_user_data_fixture():
    mock_auth_user_repository = mock_safe(AuthUserRepository)
    mock_auth_user_repository.save.side_effect = mocked_safe
    mock_crypto_context = mock_safe(CryptoContext)
    mock_crypto_context.hash_password.return_value = (
        "the_hash"  # todo remove CryptoContext mock
    )
    create_user = CreateUser(mock_auth_user_repository, mock_crypto_context)
    yield create_user, mock_auth_user_repository, mock_crypto_context


def test_create_user_successfully(create_user_data_fixture):
    (
        create_user,
        mock_auth_user_repository,
        mock_crypto_context,
    ) = create_user_data_fixture
    create_user_data = CreateUserData(username=USERNAME, fullname=FULLNAME, email=EMAIL)
    mock_auth_user_repository.exists_by_username.return_value = False
    mock_auth_user_repository.exists_by_email.return_value = False
    created_user = create_user.create_user(create_user_data)

    assert created_user == AuthUser(
        id=1, username=USERNAME, fullname=FULLNAME, email=EMAIL
    )
    mock_auth_user_repository.exists_by_username.assert_called_with(USERNAME)
    mock_auth_user_repository.exists_by_email.assert_called_with(EMAIL)
    mock_auth_user_repository.save.assert_called_with(
        AuthUser(id=1, username=USERNAME, fullname=FULLNAME, email=EMAIL)
    )


def test_create_user_should_fail_because_username_already_exists(
    create_user_data_fixture,
):
    (
        create_user,
        mock_auth_user_repository,
        mock_crypto_context,
    ) = create_user_data_fixture
    create_user_data = CreateUserData(username=USERNAME, fullname=FULLNAME, email=EMAIL)
    mock_auth_user_repository.exists_by_username.return_value = True
    mock_auth_user_repository.exists_by_email.return_value = False

    with pytest.raises(UsernameAlreadyExistsException):
        create_user.create_user(create_user_data)

    mock_auth_user_repository.exists_by_username.assert_called_with(USERNAME)
    mock_auth_user_repository.exists_by_email.assert_not_called()
    mock_auth_user_repository.save.assert_not_called()


def test_create_user_should_fail_because_email_already_exists(
    create_user_data_fixture,
):
    (
        create_user,
        mock_auth_user_repository,
        mock_crypto_context,
    ) = create_user_data_fixture
    create_user_data = CreateUserData(username=USERNAME, fullname=FULLNAME, email=EMAIL)
    mock_auth_user_repository.exists_by_username.return_value = False
    mock_auth_user_repository.exists_by_email.return_value = True

    with pytest.raises(EmailAlreadyExistsException):
        create_user.create_user(create_user_data)

    mock_auth_user_repository.exists_by_username.assert_called_with(USERNAME)
    mock_auth_user_repository.exists_by_email.assert_called_with(EMAIL)
    mock_auth_user_repository.save.assert_not_called()


def test_create_or_update_user_should_create_user(create_user_data_fixture):
    (
        create_user,
        mock_auth_user_repository,
        mock_crypto_context,
    ) = create_user_data_fixture
    mock_auth_user_repository.find_by_username.return_value = None
    expected_created_user = AuthUser(
        id=1, username=USERNAME, fullname=FULLNAME, email=EMAIL
    )
    create_user.create_user = mock.MagicMock(return_value=expected_created_user)
    create_user_data = CreateUserData(username=USERNAME, fullname=FULLNAME, email=EMAIL)

    created_user = create_user.create_or_update_user(create_user_data)

    create_user.create_user.assert_called_with(create_user_data)
    assert created_user == expected_created_user


def test_create_or_update_user_should_update_user(create_user_data_fixture):
    (
        create_user,
        mock_auth_user_repository,
        mock_crypto_context,
    ) = create_user_data_fixture
    mock_auth_user_repository.find_by_username.return_value = AuthUser(
        id=1, username=USERNAME, fullname=FULLNAME, email=EMAIL
    )
    create_user_data = CreateUserData(
        username=USERNAME, fullname=Username("Newton Username"), email=EMAIL
    )
    create_user.create_user = mock.MagicMock()

    updated_user = create_user.create_or_update_user(create_user_data)

    assert updated_user == AuthUser(
        id=1, username=USERNAME, fullname=Username("Newton Username"), email=EMAIL
    )
    create_user.create_user.assert_not_called()
