import datetime

import humanfriendly

from cato_common.domain.auth.api_token_name import ApiTokenName
from cato_server.authentication.create_api_token import CreateApiTokenData


class UserCliInput:
    def __init__(self, get_input=input):
        self._get_input = get_input

    def prompt_create_api_token_data(self) -> CreateApiTokenData:
        token_name = self._get_input("Enter token name: ")
        self._require_not_blank_str(token_name, "ApiTokenName")
        token_lifetime_str = self._get_input(
            "Enter token lifetime (format: 1 sec|min|hour|day|year): "
        )
        self._require_not_blank_str(token_lifetime_str, "ApiTokenLifetime")

        life_time = datetime.timedelta(
            seconds=humanfriendly.parse_timespan(token_lifetime_str)
        )

        return CreateApiTokenData(name=ApiTokenName(token_name), life_time=life_time)

    def _require_not_blank_str(self, the_str: str, name: str) -> str:
        stripped = the_str.strip()
        if not stripped:
            raise ValueError(f"{name} can not be empty or blank.")
        return stripped
