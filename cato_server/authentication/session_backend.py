import datetime
import logging
from typing import Optional

from cato_server.configuration.session_configuration import SessionConfiguration
from cato_server.domain.auth.auth_user import AuthUser
from cato_server.domain.auth.session import Session
from cato_server.domain.auth.session_id import SessionId


from cato_server.storage.abstract.session_repository import SessionRepository


class SessionBackend:
    def __init__(
        self,
        session_repository: SessionRepository,
        session_configuration: SessionConfiguration,
    ):
        self._session_repository = session_repository
        self._session_configuration = session_configuration

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
            expires_at=datetime.datetime.now() + self._session_configuration.lifetime,
        )
        return self._session_repository.save(session)

    def logout_from_session(self, session: Session) -> None:
        try:
            self._session_repository.delete_by_id(session.id)
        except ValueError as e:
            logging.warning(e)
            pass
