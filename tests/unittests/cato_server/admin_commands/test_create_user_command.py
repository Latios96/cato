from cato_server.admin_commands.create_user_command import CreateUserCommand
from cato_server.admin_commands.user_cli_input import UserCliInput
from cato_server.authentication.create_user import CreateUser, CreateUserData
from cato_server.domain.auth.secret_str import SecretStr
from cato_server.domain.auth.username import Username
from tests.utils import mock_safe


def test_create_user_successfully():
    mock_create_user = mock_safe(CreateUser)
    mock_user_cli_input = mock_safe(UserCliInput)
    create_user_command = CreateUserCommand(mock_create_user, mock_user_cli_input)
    create_user_data = CreateUserData(
        username=Username("a username"),
        fullname=Username("User Username"),
        password=SecretStr("password"),
    )
    mock_user_cli_input.prompt_create_user_data.return_value = create_user_data

    create_user_command.create_user()

    mock_create_user.create_user.assert_called_with(create_user_data)
