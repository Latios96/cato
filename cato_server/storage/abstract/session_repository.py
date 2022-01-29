import datetime

from cato_server.domain.auth.session import Session
from cato_server.domain.auth.session_id import SessionId
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class SessionRepository(AbstractRepository[Session, SessionId]):
    def find_by_expires_at_is_older_than(self, date: datetime.datetime):
        pass
