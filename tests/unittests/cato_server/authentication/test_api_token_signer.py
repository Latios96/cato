import datetime

from cato_common.domain.auth.api_token_id import ApiTokenId
from cato_common.domain.auth.api_token_name import ApiTokenName
from cato_server.authentication.api_token_signer import ApiTokenSigner
from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.domain.auth.api_token import ApiToken


def test_sign_api_token(
    object_mapper,
):
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
    api_token_signer = ApiTokenSigner(
        object_mapper, AppConfigurationDefaults().create()
    )

    api_token_str = api_token_signer.sign(api_token)

    assert api_token_str.data_dict() == {
        "createdAt": created_at.isoformat(),
        "expiresAt": expires_at.isoformat(),
        "id": "ab5d20008bb1f27a1442a4da398c01712b4858d0621bef08602b76f104cef16f",
        "name": "test",
    }
