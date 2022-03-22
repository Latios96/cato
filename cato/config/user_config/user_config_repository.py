import json
import os.path
from cato.config.user_config.user_config import UserConfig

import logging

from cato_common.domain.auth.api_token_str import ApiTokenStr

logger = logging.getLogger(__name__)


class UserConfigRepository:
    def __init__(self, path: str):
        self._path = path

    def read(self) -> UserConfig:
        if not os.path.exists(self._path):
            return UserConfig()

        with open(self._path, "r") as f:
            data = json.load(f)

        return UserConfig(
            api_tokens={k: ApiTokenStr(v) for k, v in data["api_tokens"].items()}
        )

    def write(self, user_config: UserConfig) -> None:
        config_folder = os.path.dirname(self._path)
        if not os.path.exists(config_folder):
            os.makedirs(config_folder)

        with open(self._path, "w") as f:
            json.dump(
                {"api_tokens": {k: str(v) for k, v in user_config.api_tokens.items()}},
                f,
            )
