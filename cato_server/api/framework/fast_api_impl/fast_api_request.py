from starlette.requests import Request

from cato_server.api.framework.abstract.request import AbstractRequest


class FastApiRequest(AbstractRequest):
    def __init__(self, request: Request):
        self._request = request

    async def json(self):
        return await self._request.json()
