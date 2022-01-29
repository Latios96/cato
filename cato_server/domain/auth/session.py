import datetime
from dataclasses import dataclass

from cato_server.domain.auth.session_token import SessionToken


@dataclass
class Session:
    id: int
    session_token: SessionToken
    user_id: int
    created_at: datetime.datetime
    expires_at: datetime.datetime
