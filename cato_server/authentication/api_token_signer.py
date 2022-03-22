from base64 import b64encode, b64decode
import datetime

import itsdangerous
from itsdangerous import BadSignature

from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.domain.auth.api_token import ApiToken


class InvalidApiTokenException(Exception):
    pass


class ApiTokenSigner:
    def __init__(
        self, object_mapper: ObjectMapper, app_configuration: AppConfiguration
    ):
        self._object_mapper = object_mapper
        self._signer = itsdangerous.TimestampSigner(
            app_configuration.secret.get_secret_value()
        )

    def sign(self, api_token: ApiToken) -> ApiTokenStr:
        json_str = self._object_mapper.to_json(api_token)

        data = b64encode(json_str.encode("utf-8"))
        signed_data = self._signer.sign(data)

        return ApiTokenStr(signed_data)

    def unsign(self, api_token_str: ApiTokenStr):
        try:
            signed_data = self._signer.unsign(str(api_token_str))
        except BadSignature as e:
            raise InvalidApiTokenException("The token is not valid.") from e
        json_str = b64decode(signed_data).decode("utf-8")
        api_token = self._object_mapper.from_json(json_str, ApiToken)

        now = datetime.datetime.now()
        remaining_session_time = api_token.expires_at - now
        is_expired = remaining_session_time.total_seconds() <= 0
        if is_expired:
            raise InvalidApiTokenException("The token expired.")

        return api_token
