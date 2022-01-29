from cato_server.domain.auth.session import Session
from cato_server.domain.auth.session_token import SessionToken
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class SessionRepository(AbstractRepository[Session, int]):
    def find_by_session_token(self, session_token: SessionToken):
        pass
