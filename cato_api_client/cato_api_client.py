import logging
import os
from typing import Optional, Dict
from urllib.parse import quote

import requests
from requests import Response

import cato_api_client.api_client_logging  # noqa: F401
from cato.domain.project import Project
from cato.domain.run import Run
from cato.domain.test_identifier import TestIdentifier
from cato.mappers.abstract_class_mapper import AbstractClassMapper
from cato.mappers.file_class_mapper import FileClassMapper
from cato.mappers.project_class_mapper import ProjectClassMapper
from cato.mappers.run_class_mapper import RunClassMapper
from cato.mappers.suite_result_class_mapper import SuiteResultClassMapper
from cato.mappers.test_result_class_mapper import TestResultClassMapper
from cato_server.storage.domain.File import File
from cato_server.storage.domain.suite_result import SuiteResult
from cato_server.storage.domain.test_result import TestResult
from cato_api_client.http_template import HttpTemplate, AbstractHttpTemplate

logger = logging.getLogger(__name__)


class DictMapper(AbstractClassMapper):
    def map_from_dict(self, json_data: Dict) -> Dict:
        return json_data

    def map_to_dict(self, the_dict: Dict) -> Dict:
        return the_dict


class CatoApiClient:
    @staticmethod
    def from_url(url: str):
        return CatoApiClient(url, HttpTemplate())

    @staticmethod
    def from_hostname_and_port(hostname: str, port: int):
        return CatoApiClient(f"http://{hostname}:{port}", HttpTemplate())

    def __init__(self, url, http_template: AbstractHttpTemplate):
        self._url = url
        if not http_template:
            self._http_template = HttpTemplate()
        else:
            self._http_template = http_template

    def get_project_by_name(self, project_name: str) -> Optional[Project]:
        url = self._build_url("/api/v1/projects/name/{}".format(project_name))
        return self._find_with_http_template(url, ProjectClassMapper())

    def create_project(self, project_name) -> Project:
        url = self._build_url("/api/v1/projects")
        logger.info("Creating project with name %s..", project_name)
        return self._create_with_http_template(
            url, {"name": project_name}, DictMapper(), ProjectClassMapper()
        )

    def upload_file(self, path: str) -> File:
        if not os.path.exists(path):
            raise ValueError(f"Path {path} does not exists!")

        url = self._build_url("/api/v1/files")
        files = {"file": open(path, "rb")}

        logger.info("Uploading file %s", path)
        response = self._post_form(url, {}, files=files)

        if response.status_code == 201:
            return FileClassMapper().map_from_dict(self._get_json(response))
        raise self._create_value_error_for_bad_request(response)

    def create_suite_result(self, suite_result: SuiteResult) -> SuiteResult:
        if suite_result.id:
            raise ValueError(f"Id of SuiteResult is not 0, was {suite_result.id}")

        url = self._build_url("/api/v1/suite_results")
        logger.info("Creating suite_result with data %s..", suite_result)
        return self._create_with_http_template(
            url, suite_result, SuiteResultClassMapper(), SuiteResultClassMapper()
        )

    def create_run(self, run: Run) -> Run:
        if run.id:
            raise ValueError(f"Id of Run is not 0, was {run.id}")

        url = self._build_url("/api/v1/runs")
        logger.info("Creating run with data %s..", run)
        return self._create_with_http_template(
            url, run, RunClassMapper(), RunClassMapper()
        )

    def create_test_result(self, test_result: TestResult):
        if test_result.id:
            raise ValueError(f"Id of TestResult is not 0, was {test_result.id}")

        url = self._build_url("/api/v1/test_results")
        logger.info("Creating test_result with data %s..", test_result)
        return self._create_with_http_template(
            url, test_result, TestResultClassMapper(), TestResultClassMapper()
        )

    def find_test_result_by_run_id_and_identifier(
        self, run_id: int, test_identifier: TestIdentifier
    ) -> Optional[TestResult]:
        url = self._build_url(
            "/api/v1/test_results/runs/{}/{}/{}".format(
                run_id, test_identifier.suite_name, test_identifier.test_name
            )
        )
        return self._find_with_http_template(url, TestResultClassMapper())

    def update_test_result(self, test_result):
        url = self._build_url(f"/api/v1/test_results/{test_result.id}")
        return self._patch_with_http_template(
            url, test_result, TestResultClassMapper(), TestResultClassMapper()
        )

    def _build_url(self, url):
        return self._url + quote(url)

    def _get_json(self, reponse):
        return reponse.json()

    def _create_with_http_template(
        self,
        url,
        body,
        body_mapper: AbstractClassMapper,
        entity_mapper: AbstractClassMapper,
    ):
        response = self._http_template.post_for_entity(
            url, body, body_mapper, entity_mapper
        )
        if response.status_code() == 201:
            return response.get_entity()
        raise ValueError(
            "Bad parameters: {}".format(
                " ".join(
                    [
                        "{}: {}".format(key, value)
                        for key, value in response.get_json().items()
                    ]
                )
            )
        )

    def _patch_with_http_template(
        self,
        url,
        body,
        body_mapper: AbstractClassMapper,
        entity_mapper: AbstractClassMapper,
    ):
        response = self._http_template.patch_for_entity(
            url, body, body_mapper, entity_mapper
        )
        if response.status_code() == 200:
            return response.get_entity()
        raise ValueError(
            "Bad parameters: {}".format(
                " ".join(
                    [
                        "{}: {}".format(key, value)
                        for key, value in response.get_json().items()
                    ]
                )
            )
        )

    def _create_value_error_for_bad_request(self, response):
        return ValueError(
            "Bad parameters: {}".format(
                " ".join(
                    [
                        "{}: {}".format(key, value)
                        for key, value in self._get_json(response).items()
                    ]
                )
            )
        )

    def _post_form(self, url, params, files=None):
        logger.debug("Launching POST request to %s with params %s", url, params)
        response = requests.post(url, data=params, files=files)
        logger.debug("Received response %s", response)
        return response

    def _find_with_http_template(self, url, entity_mapper: AbstractClassMapper):
        response = self._http_template.get_for_entity(url, entity_mapper)
        if response.status_code() == 404:
            return None
        if response.status_code() == 200:
            return response.get_entity()
        raise ValueError(
            "Bad parameters: {}".format(
                " ".join(
                    [
                        "{}: {}".format(key, value)
                        for key, value in response.get_json().items()
                    ]
                )
            )
        )
