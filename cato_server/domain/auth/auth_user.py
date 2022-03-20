from dataclasses import dataclass

from cato_common.domain.auth.email import Email
from cato_common.domain.auth.username import Username


@dataclass
class AuthUser:
    id: int
    username: Username
    fullname: Username
    email: Email
