import datetime
from typing import Optional

from cato_server.domain.auth.auth_user import AuthUser
from cato_server.domain.auth.session import Session
from cato_server.domain.auth.session_id import SessionId


from cato_server.storage.abstract.session_repository import SessionRepository

SESSION_LIFETIME = datetime.timedelta(hours=2)


class SessionBackend:
    def __init__(self, session_repository: SessionRepository):
        self._session_repository = session_repository

    def get_session(self, id: SessionId) -> Optional[Session]:
        session = self._session_repository.find_by_id(id)
        if not session:
            return None

        now = datetime.datetime.now()
        remaining_session_time = session.expires_at - now
        is_expired = remaining_session_time.total_seconds() <= 0
        if is_expired:
            return None

        return session

    def create_session(self, user: AuthUser) -> Session:
        session = Session(
            id=SessionId.none(),
            user_id=user.id,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now() + SESSION_LIFETIME,
        )
        return self._session_repository.save(session)
