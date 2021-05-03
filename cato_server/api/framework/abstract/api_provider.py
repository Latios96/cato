from cato_server.api.framework.abstract.api_resource import AbstractBaseResource
from cato_server.api.framework.abstract.test_client import AbstractTestClient


class AbstractApiProvider:
    def register_resource(
        self, resource: AbstractBaseResource, url_prefix: str
    ) -> None:
        raise NotImplementedError()

    def run(self) -> None:
        raise NotImplementedError()

    def test_client(self) -> AbstractTestClient:
        raise NotImplementedError()

    def _verify_url_prefix(self, url_prefix: str) -> None:
        if url_prefix and url_prefix[-1] == "/":
            raise ValueError(f"url prefix can not end with '/', was '{url_prefix}'")
