from typing import Dict

from requests import Response
from starlette.testclient import TestClient

from cato_server.api.framework.abstract.test_client import (
    AbstractTestClient,
    AbstractResponse,
)


class FastApiResponse(AbstractResponse):
    def __init__(self, response: Response):
        self._response = response

    @property
    def json(self) -> Dict:
        return self._response.json()

    @property
    def status_code(self) -> int:
        return self._response.status_code


class FastApiTestClient(AbstractTestClient):
    def __init__(self, test_client: TestClient):
        self._test_client = test_client

    def get(self, url: str) -> AbstractResponse:
        return FastApiResponse(self._test_client.get(url))

    def post(self, url: str) -> AbstractResponse:
        return FastApiResponse(self._test_client.post(url))
