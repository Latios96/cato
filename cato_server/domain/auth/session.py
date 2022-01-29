import datetime
from dataclasses import dataclass

from cato_server.domain.auth.session_id import SessionId


@dataclass
class Session:
    id: SessionId
    user_id: int
    created_at: datetime.datetime
    expires_at: datetime.datetime
