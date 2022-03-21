import datetime

import pytest
from itsdangerous import BadTimeSignature

from cato_common.domain.auth.api_token_id import ApiTokenId
from cato_common.domain.auth.api_token_name import ApiTokenName
from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_server.authentication.api_token_signer import ApiTokenSigner
from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.domain.auth.api_token import ApiToken
from cato_server.domain.auth.secret_str import SecretStr


@pytest.fixture
def api_token_signer(object_mapper):
    app_config = AppConfigurationDefaults().create()
    app_config.secret = SecretStr(
        "31f4e380d9ab4e443d762f73d0f1b14c7eadf52b4735663a485a0f31f95c3267"
    )
    api_token_signer = ApiTokenSigner(object_mapper, app_config)
    return api_token_signer


def test_sign_api_token(object_mapper, api_token_signer):
    token_id = ApiTokenId(
        "ab5d20008bb1f27a1442a4da398c01712b4858d0621bef08602b76f104cef16f"
    )
    created_at = datetime.datetime.now()
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


def test_unsign_valid_api_token(api_token_str, api_token_signer):
    api_token = api_token_signer.unsign(api_token_str)

    assert api_token == ApiToken(
        name=ApiTokenName("test"),
        id=ApiTokenId(
            "ab5d20008bb1f27a1442a4da398c01712b4858d0621bef08602b76f104cef16f"
        ),
        created_at=datetime.datetime(2022, 3, 21, 17, 15, 24, 328633),
        expires_at=datetime.datetime(2022, 3, 21, 19, 15, 24, 328633),
    )


def test_unsign_invalid_api_token(api_token_str, api_token_signer):
    with pytest.raises(BadTimeSignature):
        api_token_signer.unsign(ApiTokenStr(bytes(api_token_str) + b"1"))
