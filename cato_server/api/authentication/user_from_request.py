from typing import Optional

from starlette.requests import Request

from cato_server.authentication.session_backend import SessionBackend
from cato_server.domain.auth.auth_user import AuthUser


class UserFromRequest:
    def __init__(self, session_backend: SessionBackend, auth_user_repository):
        self._session_backend = session_backend
        self._auth_user_repository = auth_user_repository

    def user_from_request(self, request: Request) -> Optional[AuthUser]:
        session = self._session_backend.get_session(request.session.get("session_id"))
        if not session:
            return None
        return self._auth_user_repository.find_by_id(session.user_id)
