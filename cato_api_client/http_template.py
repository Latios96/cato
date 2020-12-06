from typing import TypeVar, Generic
from urllib.parse import quote

import requests

from cato.mappers.abstract_class_mapper import AbstractClassMapper
from cato_api_client.cato_api_client import logger

T = TypeVar("T")


class HttpTemplateResponse(Generic[T]):

    def __init__(self, response, mapper: AbstractClassMapper[T]):
        self._response = response
        self._mapper = mapper

    def status_code(self) -> int:
        raise NotImplementedError()

    def get_entity(self) -> T:
        return self._mapper.map_from_dict(self._get_json())

    def _get_json(self):
        raise NotImplementedError()


class RequestsHttpTemplateResponse(HttpTemplateResponse):

    def status_code(self):
        return self._response.status_code

    def _get_json(self):
        return self._response.json()


class HttpTemplateException(Exception):
    pass


class AbstractHttpTemplate:

    def get_for_entity(self, url: str, response_cls_mapper: AbstractClassMapper[T]) -> HttpTemplateResponse[T]:
        url = quote(url)
        logger.debug("Launching GET request to %s ", url)
        response = self._get(url)
        logger.debug("Received response %s", response)
        return self._handle_response(response, response_cls_mapper)

    def post_for_entity(self, url, body, body_cls_mapper: AbstractClassMapper[T],
                        response_cls_mapper: AbstractClassMapper, ) -> HttpTemplateResponse[T]:
        url = quote(url)
        params = body
        if body_cls_mapper:
            params = body_cls_mapper.map_to_dict(body)
        logger.debug("Launching POST request to %s with json %s", url, params)
        response = self._post(url, params)
        logger.debug("Received response %s", response)
        if response.status_code == 500:
            raise HttpTemplateException("Internal Server Error!")
        return self._construct_http_template_response(response, response_cls_mapper)

    def _handle_response(self, response, response_cls_mapper: AbstractClassMapper[T]) -> HttpTemplateResponse[T]:
        if response.status_code == 500:
            raise HttpTemplateException("Internal Server Error!")
        return self._construct_http_template_response(response, response_cls_mapper)

    def _post(self, url, params):
        raise NotImplementedError()

    def _get(self, url):
        raise NotImplementedError()

    def _construct_http_template_response(self, response, response_cls_mapper: AbstractClassMapper[T]):
        raise NotImplementedError()


class RequestsHttpTemplate(AbstractHttpTemplate):
    def _post(self, url, params):
        return requests.post(url, json=params)

    def _get(self, url):
        return requests.get(url)

    def _construct_http_template_response(self, response, response_cls_mapper):
        return RequestsHttpTemplateResponse(response, response_cls_mapper)


HttpTemplate = RequestsHttpTemplate
