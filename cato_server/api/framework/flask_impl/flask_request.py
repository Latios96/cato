from typing import Dict

from flask import request

from cato_server.api.framework.abstract.request import AbstractRequest


class FlaskRequest(AbstractRequest):
    def __init__(self, the_request: request):
        self._request = the_request

    def json(self) -> Dict:
        return self._request.get_json()
