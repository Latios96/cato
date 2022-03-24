import logging

from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from cato_server.api.authentication.user_from_request import UserFromRequest
from cato_server.authentication.api_token_signer import (
    ApiTokenSigner,
)

logger = logging.getLogger(__name__)

FORCE = False


class AuthenticationMiddleware:
    def __init__(
        self, api_token_signer: ApiTokenSigner, user_from_request: UserFromRequest
    ):
        self._api_token_signer = api_token_signer
        self._user_from_request = user_from_request

    async def __call__(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if self._is_unprotected_route(request):
            return await call_next(request)

        has_valid_api_token = self._user_from_request.api_token_from_request(request)
        if has_valid_api_token:
            return await call_next(request)

        has_valid_session = self._user_from_request.session_from_request(request)
        if not has_valid_session:
            return Response(status_code=401)

        return await call_next(request)

    def _is_unprotected_route(self, request: Request):
        request_route = request.url.path
        if request_route in {"/", "/index.html"}:
            return True
        unprotected_routes = ["/login", "/auth", "/static"]
        for unprotected_route in unprotected_routes:
            if request_route.startswith(unprotected_route):
                return True
        return False
