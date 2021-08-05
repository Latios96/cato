import logging
from typing import TypeVar, Generic, Type, List

import requests

from cato_common.mappers.object_mapper import ObjectMapper

logger = logging.getLogger(__name__)

B = TypeVar("B")
R = TypeVar("R")


class HttpTemplateResponse(Generic[R]):
    def __init__(self, response_cls: Type[R], mapper: ObjectMapper) -> None:
        self._mapper = mapper
        self._response_cls = response_cls

    def status_code(self) -> int:
        raise NotImplementedError()

    def get_entity(self) -> R:
        json = self.get_json()
        if json:
            return self._mapper.from_dict(json, self._response_cls)
        raise ValueError("Json is None!")

    def get_entities(self) -> List[R]:
        return self._mapper.many_from_dict(self.get_json(), self._response_cls)

    def get_json(self):
        raise NotImplementedError()

    def text(self):
        raise NotImplementedError()


class RequestsHttpTemplateResponse(HttpTemplateResponse):
    def __init__(
        self, response: requests.Response, response_cls: Type[R], mapper: ObjectMapper
    ) -> None:
        super(RequestsHttpTemplateResponse, self).__init__(response_cls, mapper)
        self._response = response

    def status_code(self):
        return self._response.status_code

    def get_json(self):
        return self._response.json()

    def __str__(self):
        return str(self._response)

    def text(self):
        return self._response.text


class HttpTemplateException(Exception):
    pass


class AbstractHttpTemplate:
    def __init__(self, object_mapper: ObjectMapper):
        self._object_mapper = object_mapper

    def get_for_entity(
        self, url: str, response_cls: Type[R]
    ) -> HttpTemplateResponse[R]:
        logger.debug("Launching GET request to %s ", url)
        response = self._get(url)
        logger.debug("Received response %s", response)
        return self._handle_response(response, response_cls)

    def post_for_entity(
        self,
        url: str,
        body: B,
        response_cls: Type[R],
    ) -> HttpTemplateResponse[R]:
        return self._launch_request_with_body(url, body, response_cls, "POST")

    def patch_for_entity(
        self,
        url: str,
        body: B,
        response_cls: Type[R],
    ) -> HttpTemplateResponse[R]:
        return self._launch_request_with_body(url, body, response_cls, "PATCH")

    def _launch_request_with_body(
        self,
        url: str,
        body: B,
        response_cls: Type[R],
        method: str,
    ) -> HttpTemplateResponse[R]:
        method = method.upper()
        params = self._object_mapper.to_dict(body)
        logger.debug("Launching %s request to %s with json %s", method, url, params)
        assert method in ["POST", "PATCH"]
        if method == "POST":
            response = self._post(url, params)
        else:
            response = self._patch(url, params)
        logger.debug("Received response %s", response)
        if response.status_code == 500:
            raise HttpTemplateException("Internal Server Error!")
        return self._construct_http_template_response(response, response_cls)

    def _handle_response(
        self, response: HttpTemplateResponse, response_cls: Type[R]
    ) -> HttpTemplateResponse[R]:
        if response.status_code == 500:
            raise HttpTemplateException("Internal Server Error!")
        return self._construct_http_template_response(response, response_cls)

    def _post(self, url, params):
        raise NotImplementedError()

    def _get(self, url):
        raise NotImplementedError()

    def _patch(self, url, params):
        raise NotImplementedError()

    def _construct_http_template_response(
        self, response: HttpTemplateResponse, response_cls: Type[R]
    ) -> HttpTemplateResponse[R]:
        raise NotImplementedError()


class RequestsHttpTemplate(AbstractHttpTemplate):
    def _post(self, url, params):
        return requests.post(url, json=params)

    def _get(self, url):
        return requests.get(url)

    def _patch(self, url, params):
        return requests.patch(url, json=params)

    def _construct_http_template_response(self, response, response_cls_mapper):
        return RequestsHttpTemplateResponse(
            response, response_cls_mapper, self._object_mapper
        )


HttpTemplate = RequestsHttpTemplate
