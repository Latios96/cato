from collections import Callable


class AbstractBaseResource:
    def add_route(self, url: str, method: str, handler: Callable) -> None:
        raise NotImplementedError()
