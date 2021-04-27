import uvicorn
from fastapi import FastAPI
from starlette.testclient import TestClient

from cato_server.api.framework.abstract.api_provider import AbstractApiProvider
from cato_server.api.framework.abstract.api_resource import AbstractBaseResource


class FastApiApiProvider(AbstractApiProvider):

    def __init__(self):
        super(FastApiApiProvider, self).__init__()
        self._app = FastAPI()

    def register_resource(self, resource: AbstractBaseResource, url_prefix: str):
        self._app.include_router(resource, prefix=url_prefix)

    def run(self):
        uvicorn.run(self._app, host="0.0.0.0", port=5000)

    def test_client(self):
        return TestClient(self._app)