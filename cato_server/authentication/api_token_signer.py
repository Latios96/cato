from base64 import b64encode

import itsdangerous

from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.domain.auth.api_token import ApiToken


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
