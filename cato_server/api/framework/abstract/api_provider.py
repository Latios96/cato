from cato_server.api.base_resource import AbstractBaseResource


class AbstractApiProvider:

    def register_resource(self, resource: AbstractBaseResource, url_prefix: str)->None:
        raise NotImplementedError()

    def run(self)->None:
        raise NotImplementedError()

    def test_client(self):
        raise NotImplementedError()