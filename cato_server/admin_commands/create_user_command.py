from cato_server.admin_commands.user_cli_input import UserCliInput
from cato_server.authentication.create_user import CreateUser


class CreateUserCommand:
    def __init__(self, create_user: CreateUser, user_cli_input: UserCliInput):
        self._create_user = create_user
        self._user_cli_input = user_cli_input

    def create_user(self):
        create_user_data = self._user_cli_input.prompt_create_user_data()
        # todo prompt if you are sure
        self._create_user.create_user(create_user_data)
