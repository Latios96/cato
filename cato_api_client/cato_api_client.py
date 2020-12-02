from typing import Optional
from urllib.parse import quote

import requests
from requests import Response

from cato.domain.project import Project
from cato_api_client.api_client_logging import logger


class CatoApiClient:

    @staticmethod
    def from_url(url: str):
        return CatoApiClient(url)

    @staticmethod
    def from_hostname_and_port(hostname: str, port: int):
        return CatoApiClient(f"http://{hostname}:{port}")

    def __init__(self, url):
        self._url = url

    def get_project_by_name(self, project_name: str) -> Optional[Project]:
        url = self._build_url("/api/v1/projects/name/{}", project_name)
        return self._get_one_project(url)

    def create_project(self, project_name) -> Project:
        url = self._build_url("/api/v1/projects")
        return self._create(url, {'name': project_name}, Project)

    def _build_url(self, url_template, *params: str):
        params = list(map(lambda x: quote(x), params))
        return self._url + url_template.format(*params)

    def _get_one_project(self, url) -> Optional[Project]:
        response = self._get(url)
        if response.status_code == 404:
            return None
        data = self._get_json(response)
        return Project(**data)

    def _get(self, url: str) -> Response:
        logger.debug("Launching GET request to %s", url)
        return requests.get(url)

    def _get_json(self, reponse):
        return reponse.json()

    def _create(self, url, params, cls):
        response = self._post(url, params)
        if response.status_code == 201:
            return cls(**self._get_json(response))
        raise self._create_value_error_for_bad_request(response)

    def _create_value_error_for_bad_request(self, response):
        return ValueError("Bad parameters: {}".format(
            " ".join(["{}: {}".format(key, value) for key, value in self._get_json(response).items()])))

    def _post(self, url, params):
        logger.debug("Launching POST request to %s with params %s", url, params)
        return requests.post(url, data=params)

