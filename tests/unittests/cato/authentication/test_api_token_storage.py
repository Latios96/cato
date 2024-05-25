import pytest

from cato.authentication.api_token_storage import (
    ApiTokenStorage,
    CATO_API_TOKEN_ENV_VARIABLE,
    NoApiTokenFound,
)
from cato_common.config.user_local_storage.user_local_storage import UserLocalStorage
from cato_common.config.user_local_storage.user_local_storage_repository import (
    UserLocalStorageRepository,
)
from cato_common.domain.auth.api_token_str import ApiTokenStr
from tests.utils import mock_safe

URL = "http://localhost:5000"


class TestGetApiTokenFromEnv:
    def test_get_api_token_from_env_success(self):
        api_token_storage = ApiTokenStorage(
            URL,
            user_local_storage_repository=mock_safe(UserLocalStorageRepository),
            env={CATO_API_TOKEN_ENV_VARIABLE: "token"},
        )

        assert api_token_storage.get_api_token_from_env() == ApiTokenStr("token")

    def test_get_api_token_from_env_failure(self):
        api_token_storage = ApiTokenStorage(
            URL,
            user_local_storage_repository=mock_safe(UserLocalStorageRepository),
            env={},
        )

        with pytest.raises(NoApiTokenFound):
            api_token_storage.get_api_token_from_env()


class TestGetApiToken:
    def test_get_api_token_from_env_success(self):
        mock_user_local_storage_repository = mock_safe(UserLocalStorageRepository)
        api_token_storage = ApiTokenStorage(
            URL,
            user_local_storage_repository=mock_user_local_storage_repository,
            env={CATO_API_TOKEN_ENV_VARIABLE: "token"},
        )

        assert api_token_storage.get_api_token() == ApiTokenStr("token")

    def test_get_api_token_from_config_success(self):
        mock_user_local_storage_repository = mock_safe(UserLocalStorageRepository)
        mock_user_local_storage_repository.read.return_value = UserLocalStorage(
            machine_info=None, api_tokens={URL: ApiTokenStr("token")}
        )
        api_token_storage = ApiTokenStorage(
            URL,
            user_local_storage_repository=mock_user_local_storage_repository,
            env={},
        )

        api_token = api_token_storage.get_api_token()

        assert api_token == ApiTokenStr("token")
        mock_user_local_storage_repository.read.assert_called_once()

    def test_get_api_token_no_token_in_env_or_config_failure(self):
        mock_user_local_storage_repository = mock_safe(UserLocalStorageRepository)
        mock_user_local_storage_repository.read.return_value = UserLocalStorage(
            machine_info=None, api_tokens={}
        )
        api_token_storage = ApiTokenStorage(
            URL,
            user_local_storage_repository=mock_user_local_storage_repository,
            env={},
        )

        with pytest.raises(NoApiTokenFound):
            api_token_storage.get_api_token()

    def test_get_api_token_no_token_config_for_url(self):
        mock_user_local_storage_repository = mock_safe(UserLocalStorageRepository)
        mock_user_local_storage_repository.read.return_value = UserLocalStorage(
            machine_info=None, api_tokens={"other_url": ApiTokenStr("token")}
        )
        api_token_storage = ApiTokenStorage(
            URL,
            user_local_storage_repository=mock_user_local_storage_repository,
            env={},
        )

        with pytest.raises(NoApiTokenFound):
            api_token_storage.get_api_token()
