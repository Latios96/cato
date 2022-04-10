import logging
from pathlib import Path

from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response, FileResponse

logger = logging.getLogger(__name__)

FORCE = False


class RedirectToFrontendMiddleware:
    async def __call__(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        if self._needs_frontend_redirect(request):
            static_files_folder = Path(__file__).parent.parent.parent / "static"
            return FileResponse(static_files_folder / request.url.path[1:])

        return await call_next(request)

    def _needs_frontend_redirect(self, request: Request):
        request_route = request.url.path
        if request_route in {"/", "/index.html"}:
            return False
        routes_with_no_frontend_redirect = [
            "/login",
            "/logout",
            "/auth",
            "/static",
            "/api",
        ]
        for route_with_no_frontend_redirect in routes_with_no_frontend_redirect:
            if request_route.startswith(route_with_no_frontend_redirect):
                return False
        return True
