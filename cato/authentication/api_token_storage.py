import os
from typing import Dict, Optional

from cato_common.config.user_local_storage.user_local_storage_repository import (
    UserLocalStorageRepository,
)
from cato_common.domain.auth.api_token_str import ApiTokenStr

CATO_API_TOKEN_ENV_VARIABLE = "CATO_API_TOKEN"


class NoApiTokenFound(Exception):
    def __init__(self):
        super(NoApiTokenFound, self).__init__("No ApiToken was found.")


class ApiTokenStorage:
    def __init__(
        self,
        url: str,
        user_local_storage_repository: UserLocalStorageRepository,
        env: Dict[str, str] = None,
    ):
        self._url = url
        self._user_local_storage_repository = user_local_storage_repository
        self._env = self._env_or_default(env)

    def _env_or_default(self, env):
        if env is None:
            return os.environ
        else:
            return env

    def get_api_token(self) -> ApiTokenStr:
        token_str = self._token_from_env()
        if token_str:
            return token_str

        token_str = self._token_from_config(self._url)
        if token_str:
            return token_str

        raise NoApiTokenFound()

    def get_api_token_from_env(self) -> ApiTokenStr:
        token_str = self._token_from_env()
        if not token_str:
            raise NoApiTokenFound()
        return token_str

    def _token_from_env(self) -> Optional[ApiTokenStr]:
        token_str = self._env.get(CATO_API_TOKEN_ENV_VARIABLE)
        if not token_str:
            return None
        return ApiTokenStr(token_str)

    def _token_from_config(self, url: str) -> Optional[ApiTokenStr]:
        user_local_storage = self._user_local_storage_repository.read()
        token_for_url = user_local_storage.api_tokens.get(url)
        if token_for_url:
            return token_for_url
        return None
