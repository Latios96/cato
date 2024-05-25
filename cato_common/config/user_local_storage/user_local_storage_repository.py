import json
import logging
import os.path

from cato.domain.machine_info_cache_entry import MachineInfoCacheEntry
from cato_common.config.user_local_storage.user_local_storage import UserLocalStorage
from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_common.mappers.object_mapper import ObjectMapper

logger = logging.getLogger(__name__)


class UserLocalStorageRepository:
    def __init__(self, path: str, object_mapper: ObjectMapper):
        self._path = path
        self._object_mapper = object_mapper

    def read(self) -> UserLocalStorage:
        if not os.path.exists(self._path):
            return UserLocalStorage()

        with open(self._path, "r") as f:
            data = json.load(f)

        api_tokens = {k: ApiTokenStr(v) for k, v in data["api_tokens"].items()}
        machine_info_cache_entry = None
        if data.get("machine_info_cache_entry"):
            machine_info_cache_entry = self._object_mapper.from_dict(
                data["machine_info_cache_entry"], MachineInfoCacheEntry
            )
        return UserLocalStorage(
            machine_info_cache_entry=machine_info_cache_entry, api_tokens=api_tokens
        )

    def write(self, user_local_storage: UserLocalStorage) -> None:
        config_folder = os.path.dirname(self._path)
        if not os.path.exists(config_folder):
            os.makedirs(config_folder)

        with open(self._path, "w") as f:
            json.dump(
                {
                    "machine_info_cache_entry": self._object_mapper.to_dict(
                        user_local_storage.machine_info_cache_entry
                    ),
                    "api_tokens": {
                        k: str(v) for k, v in user_local_storage.api_tokens.items()
                    },
                },
                f,
            )
