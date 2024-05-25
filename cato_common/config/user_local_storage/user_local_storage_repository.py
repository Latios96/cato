import dataclasses
import json
import os.path
from cato_common.config.user_local_storage.user_local_storage import UserLocalStorage

import logging

from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_common.domain.machine_info import MachineInfo

logger = logging.getLogger(__name__)


class UserLocalStorageRepository:
    def __init__(self, path: str):
        self._path = path

    def read(self) -> UserLocalStorage:
        if not os.path.exists(self._path):
            return UserLocalStorage()

        with open(self._path, "r") as f:
            data = json.load(f)

        api_tokens = {k: ApiTokenStr(v) for k, v in data["api_tokens"].items()}
        machine_info = None
        if data.get("machine_info"):
            machine_info = MachineInfo(
                cpu_name=data["machine_info"]["cpu_name"],
                cores=data["machine_info"]["cores"],
                memory=data["machine_info"]["memory"],
            )
        return UserLocalStorage(machine_info=machine_info, api_tokens=api_tokens)

    def write(self, user_local_storage: UserLocalStorage) -> None:
        config_folder = os.path.dirname(self._path)
        if not os.path.exists(config_folder):
            os.makedirs(config_folder)

        with open(self._path, "w") as f:
            json.dump(
                {
                    "machine_info": dataclasses.asdict(user_local_storage.machine_info),
                    "api_tokens": {
                        k: str(v) for k, v in user_local_storage.api_tokens.items()
                    },
                },
                f,
            )
