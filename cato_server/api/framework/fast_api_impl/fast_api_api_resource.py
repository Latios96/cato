import inspect

from fastapi import APIRouter
from starlette.requests import Request

from cato_server.api.framework.abstract.api_resource import AbstractBaseResource
from cato_server.api.framework.fast_api_impl.fast_api_request import FastApiRequest


class FastApiAbstractBaseResource(AbstractBaseResource, APIRouter):
    def __init__(self):
        super(FastApiAbstractBaseResource, self).__init__()

    def add_route(self, url, method, handler):
        # todo convert url with path params to be fast api compliant
        async def wrapped_handler(request: Request):
            # load path params from request and convert to int of needed
            # construct arguments and call
            args = inspect.getfullargspec(handler)
            constructed_args = {}
            if "request" in args.args:
                constructed_args["request"] = FastApiRequest(request)

            return await handler(**constructed_args)

        # regex um parameter zu finden:
        # "<((int|string|float|uuid):)?(\w+)>"
        #
        # suchen:
        # print(re.search(regex, test_str).groups())
        #
        # Flask Syntax zu FastApi konvertieren:
        # print(re.sub(regex, r"{\g<3>}",test_str))

        if method == "GET":
            self.get(url)(wrapped_handler)
        elif method == "POST":
            self.post(url)(wrapped_handler)
