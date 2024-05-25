import json

import pytest

from cato.domain.machine_info_cache_entry import MachineInfoCacheEntry
from cato_common.config.user_local_storage.user_local_storage import UserLocalStorage
from cato_common.config.user_local_storage.user_local_storage_repository import (
    UserLocalStorageRepository,
)
from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_common.domain.machine_info import MachineInfo
from cato_common.utils.datetime_utils import aware_now_in_utc


@pytest.fixture
def user_local_storage():
    return UserLocalStorage(
        machine_info_cache_entry=MachineInfoCacheEntry(
            MachineInfo(cpu_name="cpu", cores=56, memory=8),
            timestamp=aware_now_in_utc(),
        ),
        api_tokens={"http://localhost:5000": ApiTokenStr("test")},
    )


@pytest.fixture
def user_local_storage_path(tmp_path):
    return tmp_path / "cato_user_local_storage.json"


@pytest.fixture
def user_local_storage_repository(tmp_path, user_local_storage_path, object_mapper):
    return UserLocalStorageRepository(str(user_local_storage_path), object_mapper)


def test_write_user_local_storage(
    user_local_storage_repository, user_local_storage, user_local_storage_path
):
    assert not user_local_storage_path.exists()

    user_local_storage_repository.write(user_local_storage)

    assert user_local_storage_path.exists()
    with user_local_storage_path.open() as f:
        written_data = json.load(f)

    assert written_data["machine_info_cache_entry"].pop("timestamp") is not None
    assert written_data == {
        "api_tokens": {"http://localhost:5000": "test"},
        "machine_info_cache_entry": {
            "machineInfo": {"cores": 56, "cpuName": "cpu", "memory": 8}
        },
    }


def test_read_not_existing_user_local_storage(user_local_storage_repository):
    user_local_storage = user_local_storage_repository.read()

    assert user_local_storage == UserLocalStorage()


def test_read_existing_user_local_storage(
    user_local_storage_repository, user_local_storage
):
    user_local_storage_repository.write(user_local_storage)

    read_user_local_storage = user_local_storage_repository.read()

    assert user_local_storage == read_user_local_storage
