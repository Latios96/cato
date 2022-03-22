from itsdangerous import BadSignature
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_common.domain.auth.bearer_token import BearerToken
from cato_server.authentication.api_token_signer import ApiTokenSigner
import logging

logger = logging.getLogger(__name__)


class AuthenticationMiddleware:
    def __init__(self, api_token_signer: ApiTokenSigner):
        self._api_token_signer = api_token_signer

    async def __call__(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        api_token_str = self._read_api_token_from_request(request)
        if api_token_str:
            try:
                self._api_token_signer.unsign(api_token_str)
            except BadSignature as err:
                logger.error(err)
                return Response(status_code=401)

        return await call_next(request)

    def _read_api_token_from_request(self, request):
        header = request.headers.get("Authorization")
        if not header:
            return None

        token_str = BearerToken.parse_from_header(header)
        return ApiTokenStr.from_bearer(token_str)
