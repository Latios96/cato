import logging
from pathlib import Path

from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, RedirectResponse, FileResponse

from cato_server.api.authentication.user_from_request import UserFromRequest
from cato_server.authentication.api_token_signer import (
    ApiTokenSigner,
)

logger = logging.getLogger(__name__)

FORCE = False


class RedirectToFrontendMiddleware:

    STATIC_FILES_FOLDER = Path(__file__).parent.parent.parent / "static" / "index.html"

    async def __call__(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if self._needs_frontend_redirect(request):
            return FileResponse(self.STATIC_FILES_FOLDER)

        return await call_next(request)

    def _needs_frontend_redirect(self, request: Request):
        request_route = request.url.path
        if request_route in {"/", "/index.html"}:
            return False
        unprotected_routes = ["/login", "/logout", "/auth", "/static", "/api"]
        for unprotected_route in unprotected_routes:
            if request_route.startswith(unprotected_route):
                return False
        return True
