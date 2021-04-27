class AbstractBaseResource:

    def add_route(self, url, method, handler):
        raise NotImplementedError()