from unittest import mock

import pytest

from cato_server.admin_commands.user_cli_input import (
    UserCliInput,
    PasswordDidNotMatchException,
)


@pytest.fixture
def user_cli_input_fixture():
    mock_input = mock.MagicMock()
    mock_getpass = mock.MagicMock()
    user_cli_input = UserCliInput(mock_input, mock_getpass)
    yield user_cli_input, mock_input, mock_getpass


def test_input_username_and_password_successfully(user_cli_input_fixture):
    user_cli_input, mock_input, mock_getpass = user_cli_input_fixture
    mock_input.return_value = "a username"
    mock_getpass.return_value = "password"

    username, password = user_cli_input.prompt_username_and_password()

    assert username == "a username"
    assert password == "password"

    mock_input.assert_called_with("Enter username: ")
    assert mock_getpass.call_count == 2


def test_username_is_blank(user_cli_input_fixture):
    user_cli_input, mock_input, mock_getpass = user_cli_input_fixture
    mock_input.return_value = " "
    mock_getpass.return_value = "password"

    with pytest.raises(ValueError):
        user_cli_input.prompt_username_and_password()


def test_password_is_blank(user_cli_input_fixture):
    user_cli_input, mock_input, mock_getpass = user_cli_input_fixture
    mock_input.return_value = "username"
    mock_getpass.return_value = " "

    with pytest.raises(ValueError):
        user_cli_input.prompt_username_and_password()


def test_passwords_dont_match(user_cli_input_fixture):
    user_cli_input, mock_input, mock_getpass = user_cli_input_fixture
    mock_input.return_value = "username"
    mock_getpass.side_effect = ["password", "passwords"]

    with pytest.raises(PasswordDidNotMatchException):
        user_cli_input.prompt_username_and_password()
