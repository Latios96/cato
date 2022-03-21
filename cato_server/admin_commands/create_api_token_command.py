from cato_server.admin_commands.user_cli_input import UserCliInput
from cato_server.authentication.create_api_token import CreateApiToken

import logging

logger = logging.getLogger(__name__)


class CreateApiTokenCommand:
    def __init__(self, create_api_token: CreateApiToken, user_cli_input: UserCliInput):
        self._create_api_token = create_api_token
        self._user_cli_input = user_cli_input

    def create_api_token(self):
        create_api_token_data = self._user_cli_input.prompt_create_api_token_data()
        token = self._create_api_token.create_api_token(create_api_token_data)
        logger.info(f"Your api token is: {token}")
