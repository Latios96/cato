import datetime

import pytest

from cato_common.domain.auth.api_token_id import ApiTokenId
from cato_common.domain.auth.api_token_name import ApiTokenName
from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_server.authentication.api_token_signer import (
    ApiTokenSigner,
    InvalidApiTokenException,
)
from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.domain.auth.api_token import ApiToken
from cato_server.domain.auth.secret_str import SecretStr
from cato_common.utils.datetime_utils import aware_now_in_utc


@pytest.fixture
def secret():
    return SecretStr("31f4e380d9ab4e443d762f73d0f1b14c7eadf52b4735663a485a0f31f95c3267")


@pytest.fixture
def api_token_signer(object_mapper, secret):
    app_config = AppConfigurationDefaults().create()
    app_config.secrets_configuration.api_tokens_secret = secret
    api_token_signer = ApiTokenSigner(object_mapper, app_config.secrets_configuration)
    return api_token_signer


def test_sign_api_token(object_mapper, api_token_signer):
    token_id = ApiTokenId(
        "ab5d20008bb1f27a1442a4da398c01712b4858d0621bef08602b76f104cef16f"
    )
    created_at = aware_now_in_utc()
    expires_at = created_at + datetime.timedelta(hours=2)
    api_token = ApiToken(
        name=ApiTokenName("test"),
        id=token_id,
        created_at=created_at,
        expires_at=expires_at,
    )

    api_token_str = api_token_signer.sign(api_token)

    assert api_token_str.data_dict() == {
        "createdAt": created_at.isoformat(),
        "expiresAt": expires_at.isoformat(),
        "id": "ab5d20008bb1f27a1442a4da398c01712b4858d0621bef08602b76f104cef16f",
        "name": "test",
    }


def test_unsign_valid_api_token(api_token_str_factory, api_token_signer, secret):
    token_id = ApiTokenId(
        "379b493043dbd35fa8c22be22843993555f79b0ebbff945b8c726927612ddf50"
    )
    created_at = aware_now_in_utc()
    api_token_str = api_token_str_factory(
        id=token_id, created_at=created_at, secret=secret
    )
    api_token = api_token_signer.unsign(api_token_str)

    assert api_token == ApiToken(
        name=ApiTokenName("test"),
        id=token_id,
        created_at=created_at,
        expires_at=created_at + datetime.timedelta(hours=2),
    )


def test_unsign_valid_api_token_with_naive_datetime(
    api_token_str_factory, api_token_signer, secret
):
    token_id = ApiTokenId(
        "379b493043dbd35fa8c22be22843993555f79b0ebbff945b8c726927612ddf50"
    )
    created_at = datetime.datetime.now()
    api_token_str = api_token_str_factory(
        id=token_id, created_at=created_at, secret=secret
    )
    api_token = api_token_signer.unsign(api_token_str)

    assert api_token == ApiToken(
        name=ApiTokenName("test"),
        id=token_id,
        created_at=created_at,
        expires_at=created_at + datetime.timedelta(hours=2),
    )


def test_unsign_invalid_api_token(fixed_api_token_str, api_token_signer):
    with pytest.raises(InvalidApiTokenException):
        api_token_signer.unsign(ApiTokenStr(bytes(fixed_api_token_str) + b"1"))


def test_unsign_expired_api_token(api_token_str_factory, api_token_signer, secret):
    yesterday = aware_now_in_utc() - datetime.timedelta(days=1)
    created_at = yesterday
    api_token_str = api_token_str_factory(created_at=created_at, secret=secret)

    with pytest.raises(InvalidApiTokenException):
        api_token_signer.unsign(api_token_str)
