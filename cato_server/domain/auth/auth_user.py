from dataclasses import dataclass

from cato_server.domain.auth.secret_str import SecretStr
from cato_server.domain.auth.username import Username


@dataclass
class AuthUser:
    id: int
    username: Username
    hashed_password: SecretStr
