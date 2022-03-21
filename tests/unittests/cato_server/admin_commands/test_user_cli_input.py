import datetime
from unittest import mock

import pytest
from humanfriendly import InvalidTimespan

from cato_common.domain.auth.api_token_name import ApiTokenName
from cato_server.admin_commands.user_cli_input import (
    UserCliInput,
)
from cato_server.authentication.create_api_token import CreateApiTokenData


@pytest.fixture
def user_cli_input_fixture():
    mock_input = mock.MagicMock()
    user_cli_input = UserCliInput(mock_input)
    yield user_cli_input, mock_input


def test_input_token_data_successfully(user_cli_input_fixture):
    user_cli_input, mock_input = user_cli_input_fixture
    mock_input.side_effect = ["tokenname", "42s"]

    create_user_data = user_cli_input.prompt_create_api_token_data()

    assert create_user_data == CreateApiTokenData(
        name=ApiTokenName("tokenname"), life_time=datetime.timedelta(seconds=42)
    )

    mock_input.assert_any_call("Enter token name: ")
    mock_input.assert_any_call(
        "Enter token lifetime (format: 1 sec|min|hour|day|year): "
    )


def test_token_name_is_blank(user_cli_input_fixture):
    user_cli_input, mock_input = user_cli_input_fixture
    mock_input.return_value = " "

    with pytest.raises(ValueError):
        user_cli_input.prompt_create_api_token_data()


def test_token_lifetime_is_blank(user_cli_input_fixture):
    user_cli_input, mock_input = user_cli_input_fixture
    mock_input.side_effect = ["tokenname", " "]

    with pytest.raises(ValueError):
        user_cli_input.prompt_create_api_token_data()


def test_token_lifetime_is_not_a_timespan(user_cli_input_fixture):
    user_cli_input, mock_input = user_cli_input_fixture
    mock_input.side_effect = ["tokenname", "drölf"]

    with pytest.raises(InvalidTimespan):
        user_cli_input.prompt_create_api_token_data()
