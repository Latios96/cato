import datetime
from dataclasses import dataclass

from cato_common.domain.auth.api_token_id import ApiTokenId
from cato_common.domain.auth.api_token_name import ApiTokenName
from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_server.authentication.api_token_signer import ApiTokenSigner
from cato_server.domain.auth.api_token import ApiToken


@dataclass
class CreateApiTokenData:
    name: ApiTokenName
    life_time: datetime.timedelta


class CreateApiToken:
    def __init__(self, api_token_signer: ApiTokenSigner):
        self._api_token_signer = api_token_signer

    def create_api_token(
        self, create_api_token_data: CreateApiTokenData
    ) -> ApiTokenStr:
        self._validate_lifetime(create_api_token_data.life_time)

        token_id = ApiTokenId.generate()
        created_at = datetime.datetime.now()
        expires_at = created_at + create_api_token_data.life_time
        api_token = ApiToken(
            name=create_api_token_data.name,
            id=token_id,
            created_at=created_at,
            expires_at=expires_at,
        )
        return self._api_token_signer.sign(api_token)

    def _validate_lifetime(self, life_time):
        now = datetime.datetime.now()
        if now + life_time <= now:
            raise ValueError("The lifetime needs to be positive.")
        elif life_time.days > 365:
            raise ValueError("The maximum lifetime is one year.")