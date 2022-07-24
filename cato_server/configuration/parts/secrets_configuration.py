import secrets
from dataclasses import dataclass

from cato_server.domain.auth.secret_str import SecretStr


@dataclass
class SecretsConfiguration:
    sessions_secret: SecretStr
    csrf_secret: SecretStr
    api_tokens_secret: SecretStr

    @staticmethod
    def default():
        return SecretsConfiguration(
            sessions_secret=SecretStr(secrets.token_urlsafe()),
            csrf_secret=SecretStr(secrets.token_urlsafe()),
            api_tokens_secret=SecretStr(secrets.token_urlsafe()),
        )
