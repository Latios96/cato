from dataclasses import dataclass

from cato_server.domain.auth.email import Email
from cato_server.domain.auth.username import Username


@dataclass
class AuthUser:
    id: int
    username: Username
    fullname: Username
    email: Email
