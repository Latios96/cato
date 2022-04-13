import datetime
from unittest import mock

import pytest
from freezegun import freeze_time

from cato_common.domain.auth.api_token_id import ApiTokenId
from cato_common.domain.auth.api_token_name import ApiTokenName
from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_server.authentication.api_token_signer import ApiTokenSigner
from cato_server.authentication.create_api_token import (
    CreateApiToken,
    CreateApiTokenData,
)
from cato_server.domain.auth.api_token import ApiToken
from tests.utils import mock_safe


@pytest.fixture
def create_api_token_fixture():
    mock_api_token_signer = mock_safe(ApiTokenSigner)
    create_api_token = CreateApiToken(mock_api_token_signer)
    return create_api_token, mock_api_token_signer


@freeze_time(datetime.datetime(2022, 1, 29, 0, 0, 0, tzinfo=datetime.timezone.utc))
@mock.patch("secrets.token_hex")
def test_create_api_token(mock_token_hex, create_api_token_fixture):
    mock_token_hex.return_value = "hexhexhex"
    create_api_token, mock_api_token_signer = create_api_token_fixture
    mock_api_token_signer.sign.return_value = ApiTokenStr(b"test")
    create_api_token_data = CreateApiTokenData(
        name=ApiTokenName("test"), life_time=datetime.timedelta(hours=1)
    )

    api_token_str = create_api_token.create_api_token(create_api_token_data)

    assert api_token_str == ApiTokenStr(b"test")
    mock_api_token_signer.sign.assert_called_with(
        ApiToken(
            name=create_api_token_data.name,
            id=ApiTokenId("hexhexhex"),
            created_at=datetime.datetime(
                2022, 1, 29, 0, 0, 0, tzinfo=datetime.timezone.utc
            ),
            expires_at=datetime.datetime(
                2022, 1, 29, 1, 0, 0, tzinfo=datetime.timezone.utc
            ),
        )
    )


@pytest.mark.parametrize(
    "invalid_lifetime",
    [
        datetime.timedelta(hours=-1),
        datetime.timedelta(days=366),
        datetime.timedelta(hours=0),
    ],
)
def test_does_not_create_for_invalid_lifetime(
    invalid_lifetime, create_api_token_fixture
):
    create_api_token, mock_api_token_signer = create_api_token_fixture
    create_api_token_data = CreateApiTokenData(
        name=ApiTokenName("test"), life_time=invalid_lifetime
    )

    with pytest.raises(ValueError):
        create_api_token.create_api_token(create_api_token_data)
