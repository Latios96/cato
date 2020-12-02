import logging
from typing import Optional, List
from urllib.parse import urlencode, quote_plus

import requests
from requests import Response

from cato.domain.project import Project

logger = logging.getLogger(__name__)

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

    def _build_url(self, url_template, *params: str):
        params = list(map(lambda x: quote_plus(x), params))
        return self._url + url_template.format(*params)

    def _get_one_project(self, url) -> Optional[Project]:
        response = self._get(url)
        if response.status_code == 404:
            return None
        data = self._get_json(response)
        return Project(**data)

    def _get(self, url: str) -> Response:
        logger.info("Launching GET request to {}", url)
        return requests.get(url)

    def _get_json(self, reponse):
        return reponse.json()