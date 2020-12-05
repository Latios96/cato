import logging
# noinspection PyUnresolvedReferences
from dateutil.parser import parse

import cato_api_client.api_client_logging
import os
from typing import Optional
from urllib.parse import quote

import requests
from requests import Response

from cato.domain.project import Project
from cato.domain.run import Run
from cato.storage.domain.File import File
from cato.storage.domain.suite_result import SuiteResult

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

    def create_project(self, project_name) -> Project:
        url = self._build_url("/api/v1/projects")
        logger.info("Creating project with name %s..", project_name)
        return self._create(url, {'name': project_name}, Project)

    def upload_file(self, path: str) -> File:
        if not os.path.exists(path):
            raise ValueError(f"Path {path} does not exists!")

        url = self._build_url("/api/v1/files")
        files = {'file': open(path, 'rb')}

        logger.info("Uploading file %s", path)
        response = self._post_form(url, {}, files=files)

        if response.status_code == 201:
            return File(**self._get_json(response))
        raise self._create_value_error_for_bad_request(response)

    def create_suite_result(self, suite_result: SuiteResult) -> SuiteResult:
        if suite_result.id:
            raise ValueError(f"Id of SuiteResult is not 0, was {suite_result.id}")

        url = self._build_url("/api/v1/suite_results")
        logger.info("Creating suite_result with data %s..", suite_result)
        return self._create(url, {'run_id': suite_result.run_id,
                                  'suite_name': suite_result.suite_name,
                                  'suite_variables': suite_result.suite_variables}, SuiteResult)

    def create_run(self, run: Run) -> Run:
        if run.id:
            raise ValueError(f"Id of Run is not 0, was {run.id}")

        url = self._build_url("/api/v1/runs")
        logger.info("Creating run with data %s..", run)
        run = self._create(url, {'project_id': run.project_id,
                                  'started_at': run.started_at.isoformat()}, Run)
        run.started_at = parse(run.started_at)
        return run

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
        response = self._post_json(url, params)
        if response.status_code == 201:
            return cls(**self._get_json(response))
        raise self._create_value_error_for_bad_request(response)

    def _create_value_error_for_bad_request(self, response):
        return ValueError("Bad parameters: {}".format(
            " ".join(["{}: {}".format(key, value) for key, value in self._get_json(response).items()])))

    def _post_form(self, url, params, files=None):
        logger.debug("Launching POST request to %s with params %s", url, params)
        response = requests.post(url, data=params, files=files)
        logger.debug("Received response %s", response)
        return response

    def _post_json(self, url, params):
        logger.debug("Launching POST request to %s with json %s", url, params)
        response = requests.post(url, json=params)
        logger.debug("Received response %s", response)
        return response
