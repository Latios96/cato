import inspect
import uuid

from flask import request

from cato_server.api.base_blueprint import BaseBlueprint
from cato_server.api.framework.abstract.api_resource import AbstractBaseResource
from cato_server.api.framework.flask_impl.flask_request import FlaskRequest


class FlaskAbstractBaseResource(AbstractBaseResource, BaseBlueprint):
    def __init__(self):
        super(FlaskAbstractBaseResource, self).__init__("test", __name__)

    def add_route(self, url, method, handler):
        def my_handler():
            args = inspect.getfullargspec(handler)
            constructed_args = {}
            if "request" in args.args:
                constructed_args["request"] = FlaskRequest(request)

            return handler(**constructed_args)

        self.route(url, methods=[method], endpoint=str(uuid.uuid4()))(my_handler)
