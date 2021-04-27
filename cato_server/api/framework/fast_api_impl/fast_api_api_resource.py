from starlette.requests import Request


class FastApiAbstractBaseResource(AbstractBaseResource, APIRouter):
    def __init__(self):
        super(FastApiAbstractBaseResource, self).__init__()

    def add_route(self, url, method, handler):
        # todo convert url with path params to be fast api compliant
        async def wrapped_handler(request: Request):
            # load path params from request and convert to int of needed
            # construct arguments and call
            args = inspect.getfullargspec(handler)
            if "request" in args.args:
                return await handler(FastApiRequest(request))
            else:
                return handler()

        # regex um <(((int):)?.+)>

        if method == "GET":
            self.get(url)(wrapped_handler)