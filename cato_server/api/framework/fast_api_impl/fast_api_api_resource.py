import inspect
import re
from uuid import UUID

from fastapi import APIRouter
from starlette.requests import Request

from cato_server.api.framework.abstract.api_resource import AbstractBaseResource
from cato_server.api.framework.abstract.route_params_parser import (
    RouteParamsParser,
    RouteParamType,
)
from cato_server.api.framework.fast_api_impl.fast_api_request import FastApiRequest


class FastApiAbstractBaseResource(AbstractBaseResource, APIRouter):
    def __init__(self):
        super(FastApiAbstractBaseResource, self).__init__()
        self._route_params_parser = RouteParamsParser()

    def add_route(self, url, method, handler):

        parsed_params = self._route_params_parser.parse_route(url)
        parsed_params_by_name = {p.name: p for p in parsed_params}

        async def wrapped_handler(request: Request):
            path_params = request.path_params

            args = inspect.getfullargspec(handler)
            constructed_args = {}

            for name, value in path_params.items():
                if parsed_params_by_name.get(name).type == RouteParamType.INTEGER:
                    converted_value = int(value)
                elif parsed_params_by_name.get(name).type == RouteParamType.UUID:
                    converted_value = UUID(value)
                else:
                    converted_value = value
                constructed_args[name] = converted_value

            if "request" in args.args:
                constructed_args["request"] = FastApiRequest(request)
                return await handler(**constructed_args)

            return handler(**constructed_args)

        fast_api_route = self._route_params_parser.to_fast_api(url)

        if method == "GET":
            self.get(fast_api_route)(wrapped_handler)
        elif method == "POST":
            self.post(fast_api_route)(wrapped_handler)
