import flask
from flask_twisted import Twisted

from cato_server.api.framework.abstract.api_provider import AbstractApiProvider
from cato_server.api.framework.abstract.api_resource import AbstractBaseResource


class FlaskApiProvider(AbstractApiProvider):
    def __init__(self):
        self._app = flask.Flask(__name__, static_url_path="/")

    def register_resource(self, resource: AbstractBaseResource, url_prefix: str):
        self._app.register_blueprint(resource, url_prefix=url_prefix)

    def run(self):
        Twisted(self._app)
        print(f"Up and running on http://127.0.0.1:{5000}")
        self._app.run("127.0.0.1", 5000)

    def test_client(self):
        return self._app.test_client()