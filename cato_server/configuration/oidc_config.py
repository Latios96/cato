from dataclasses import dataclass

from cato_server.domain.auth.secret_str import SecretStr


@dataclass
class OidcConfiguration:
    client_id: str
    client_secret: SecretStr
    well_known_url: str
