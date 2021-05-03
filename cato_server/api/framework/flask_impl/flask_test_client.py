from typing import Dict


from cato_server.api.framework.abstract.test_client import (
    AbstractTestClient,
    AbstractResponse,
)


class FlaskResponse(AbstractResponse):
    def __init__(self, response):
        self._response = response

    @property
    def json(self) -> Dict:
        return self._response.json

    @property
    def status_code(self) -> int:
        return self._response.status_code


class FlaskTestClient(AbstractTestClient):
    def __init__(self, test_client):
        self._test_client = test_client

    def get(self, url: str) -> AbstractResponse:
        return FlaskResponse(self._test_client.get(url))

    def post(self, url: str, data: Dict = None) -> AbstractResponse:
        return FlaskResponse(self._test_client.post(url, json=data))
