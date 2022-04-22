import logging

from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from cato_server.storage.sqlalchemy.session_provider import (
    SessionProvider,
    within_transaction,
)

logger = logging.getLogger(__name__)


class DbSessionMiddleware:
    def __init__(self, session_provider: SessionProvider):
        self._session_provider = session_provider

    async def __call__(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        with within_transaction(self._session_provider):
            response = await call_next(request)
        return response
