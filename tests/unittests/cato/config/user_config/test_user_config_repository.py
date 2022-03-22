import pytest

from cato.config.user_config.user_config import UserConfig
from cato.config.user_config.user_config_repository import UserConfigRepository
from cato_common.domain.auth.api_token_str import ApiTokenStr


@pytest.fixture
def user_config():
    return UserConfig(api_tokens={"http://localhost:5000": ApiTokenStr("test")})


@pytest.fixture
def user_config_path(tmp_path):
    return tmp_path / "cato_user_config.json"


@pytest.fixture
def user_config_repository(tmp_path, user_config_path):
    return UserConfigRepository(str(user_config_path))


def test_write_user_config(user_config_repository, user_config, user_config_path):
    assert not user_config_path.exists()

    user_config_repository.write(user_config)

    assert user_config_path.exists()
    assert (
        user_config_path.open().read()
        == '{"api_tokens": {"http://localhost:5000": "test"}}'
    )


def test_read_not_existing_user_config(user_config_repository):
    user_config = user_config_repository.read()

    assert user_config == UserConfig()


def test_read_existing_user_config(user_config_repository, user_config):
    user_config_repository.write(user_config)

    read_user_config = user_config_repository.read()

    assert user_config == read_user_config
