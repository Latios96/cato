import pytest

from cato_common.config.user_local_storage.user_local_storage import UserLocalStorage
from cato_common.config.user_local_storage.user_local_storage_repository import (
    UserLocalStorageRepository,
)
from cato_common.domain.auth.api_token_str import ApiTokenStr


@pytest.fixture
def user_local_storage():
    return UserLocalStorage(api_tokens={"http://localhost:5000": ApiTokenStr("test")})


@pytest.fixture
def user_local_storage_path(tmp_path):
    return tmp_path / "cato_user_local_storage.json"


@pytest.fixture
def user_local_storage_repository(tmp_path, user_local_storage_path):
    return UserLocalStorageRepository(str(user_local_storage_path))


def test_write_user_local_storage(
    user_local_storage_repository, user_local_storage, user_local_storage_path
):
    assert not user_local_storage_path.exists()

    user_local_storage_repository.write(user_local_storage)

    assert user_local_storage_path.exists()
    assert (
        user_local_storage_path.open().read()
        == '{"api_tokens": {"http://localhost:5000": "test"}}'
    )


def test_read_not_existing_user_local_storage(user_local_storage_repository):
    user_local_storage = user_local_storage_repository.read()

    assert user_local_storage == UserLocalStorage()


def test_read_existing_user_local_storage(
    user_local_storage_repository, user_local_storage
):
    user_local_storage_repository.write(user_local_storage)

    read_user_local_storage = user_local_storage_repository.read()

    assert user_local_storage == read_user_local_storage
