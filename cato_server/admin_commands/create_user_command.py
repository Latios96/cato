from cato_server.admin_commands.user_cli_input import UserCliInput
from cato_server.authentication.create_user import CreateUser, CreateUserData
from cato_server.domain.auth.secret_str import SecretStr
from cato_server.domain.auth.username import Username


class CreateUserCommand:
    def __init__(self, create_user: CreateUser, user_cli_input: UserCliInput):
        self._create_user = create_user
        self._user_cli_input = user_cli_input

    def create_user(self):
        username, password = self._user_cli_input.prompt_username_and_password()

        create_user_data = CreateUserData(
            username=Username(username), password=SecretStr(password)
        )

        self._create_user.create_user(create_user_data)
