from typing import Optional

from starlette.requests import Request

from cato import logger
from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_common.domain.auth.bearer_token import BearerToken
from cato_server.authentication.api_token_signer import (
    InvalidApiTokenException,
    ApiTokenSigner,
)
from cato_server.authentication.session_backend import SessionBackend
from cato_server.domain.auth.api_token import ApiToken
from cato_server.domain.auth.auth_user import AuthUser
from cato_server.domain.auth.session import Session

# todo rename this to AuthenticationFromRequest?
from cato_server.domain.auth.session_id import SessionId
from cato_server.storage.abstract.auth_user_repository import AuthUserRepository


class UserFromRequest:
    def __init__(
        self,
        session_backend: SessionBackend,
        auth_user_repository: AuthUserRepository,
        api_token_signer: ApiTokenSigner,
    ):
        self._session_backend = session_backend
        self._auth_user_repository = auth_user_repository
        self._api_token_signer = api_token_signer

    def user_from_request(self, request: Request) -> Optional[AuthUser]:
        session = self.session_from_request(request)
        if not session:
            return None
        return self._auth_user_repository.find_by_id(session.user_id)

    def session_from_request(self, request: Request) -> Optional[Session]:
        session_id_str = request.session.get("session_id")
        if not session_id_str:
            return None
        session_id = SessionId(session_id_str)
        session = self._session_backend.get_session(session_id)
        return session

    def api_token_from_request(self, request: Request) -> Optional[ApiToken]:
        api_token_str = self._read_api_token_from_request(request)
        if not api_token_str:
            return None
        try:
            return self._api_token_signer.unsign(api_token_str)
        except InvalidApiTokenException as err:
            logger.error(err)
            return None

    def _read_api_token_from_request(self, request):
        header = request.headers.get("authorization")
        if not header:
            return None

        token_str = BearerToken.parse_from_header(header)
        return ApiTokenStr.from_bearer(token_str)
