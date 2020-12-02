import os
from typing import Optional
from urllib.parse import quote

import requests
from requests import Response

from cato.domain.project import Project
from cato.storage.domain.File import File
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

    def upload_file(self, path: str) -> File:
        if not os.path.exists(path):
            raise ValueError(f"Path {path} does not exists!")

        url = self._build_url("/api/v1/files")
        files = {'file': open(path, 'rb')}

        response = self._post(url, {}, files=files)

        if response.status_code == 201:
            return File(**self._get_json(response))
        raise self._create_value_error_for_bad_request(response)

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
        response = requests.get(url)
        logger.debug("Received response %s", response)
        return response

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

    def _post(self, url, params, files=None):
        logger.debug("Launching POST request to %s with params %s", url, params)
        response = requests.post(url, data=params, files=files)
        logger.debug("Received response %s", response)
        return response
