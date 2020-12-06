import dataclasses
import logging
# noinspection PyUnresolvedReferences
from dateutil.parser import parse

import cato_api_client.api_client_logging  # noqa: F401
import os
from typing import Optional, Dict
from urllib.parse import quote

import requests
from requests import Response

from cato.domain.machine_info import MachineInfo
from cato.domain.project import Project
from cato.domain.run import Run
from cato.domain.test_identifier import TestIdentifier
from cato.mappers.abstract_class_mapper import AbstractClassMapper, T
from cato.mappers.project_class_mapper import ProjectMapper
from cato.mappers.run_class_mapper import RunClassMapper
from cato.mappers.suite_result_class_mapper import SuiteResultClassMapper
from cato.mappers.test_result_class_mapper import TestResultClassMapper
from cato.storage.domain.File import File
from cato.storage.domain.suite_result import SuiteResult
from cato.storage.domain.test_result import TestResult
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
        url = "/api/v1/projects/name/{}".format(project_name)
        response = self._http_template.get_for_entity(url, ProjectMapper())
        if response.status_code() == 200:
            return response.get_entity()

    def create_project(self, project_name) -> Project:
        url = "/api/v1/projects"
        logger.info("Creating project with name %s..", project_name)
        return self._create_with_http_template(url, {'name': project_name}, DictMapper(), ProjectMapper())

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

        url = "/api/v1/suite_results"
        logger.info("Creating suite_result with data %s..", suite_result)
        return self._create_with_http_template(url, suite_result, SuiteResultClassMapper(), SuiteResultClassMapper())

    def create_run(self, run: Run) -> Run:
        if run.id:
            raise ValueError(f"Id of Run is not 0, was {run.id}")

        url = "/api/v1/runs"
        logger.info("Creating run with data %s..", run)
        return self._create_with_http_template(url, run, RunClassMapper(), RunClassMapper())

    def create_test_result(self, test_result: TestResult):
        if test_result.id:
            raise ValueError(f"Id of TestResult is not 0, was {test_result.id}")

        url = self._build_url("/api/v1/test_results")
        logger.info("Creating test_result with data %s..", test_result)
        data = {
            "suite_result_id": test_result.suite_result_id,
            "test_name": test_result.test_name,
            "test_identifier": str(test_result.test_identifier),
            "test_command": test_result.test_command,
            "test_variables": test_result.test_variables,
            "machine_info": dataclasses.asdict(test_result.machine_info),
            "execution_status": test_result.execution_status.name,
        }
        if test_result.status:
            data["status"] = test_result.status.name
        if test_result.output:
            data["output"] = test_result.output
        if test_result.seconds:
            data["seconds"] = test_result.seconds
        if test_result.message:
            data["message"] = test_result.message
        if test_result.image_output:
            data["image_output"] = test_result.image_output
        if test_result.reference_image:
            data["reference_image"] = test_result.reference_image
        if test_result.started_at:
            data["started_at"] = test_result.started_at
        if test_result.finished_at:
            data["finished_at"] = test_result.finished_at
        test_result = self._create(url, data, TestResult)
        test_result.test_identifier = TestIdentifier.from_string(test_result.test_identifier)
        test_result.machine_info = MachineInfo(test_result.machine_info['cpu_name'], test_result.machine_info['cores'],
                                               test_result.machine_info['memory'])
        test_result.started_at = parse(test_result.started_at) if test_result.started_at else None
        test_result.finished_at = parse(test_result.finished_at) if test_result.finished_at else None
        return test_result

    def find_test_result_by_run_id_and_identifier(self, run_id: int, test_identifier: TestIdentifier) -> Optional[
        TestResult]:
        url = self._build_url('/api/v1/test_results/runs/{}/{}/{}', str(run_id), test_identifier.suite_name,
                              test_identifier.test_name)
        response = self._get(url)
        if response.status_code == 404:
            return None
        data = self._get_json(response)
        return TestResultClassMapper().map_from_dict(data)

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

    def _create_with_http_template(self, url, body, body_mapper: AbstractClassMapper,
                                   entity_mapper: AbstractClassMapper):
        response = self._http_template.post_for_entity(url, body, body_mapper, entity_mapper)
        if response.status_code() == 201:
            return response.get_entity()
        raise ValueError("Bad parameters: {}".format(
            " ".join(["{}: {}".format(key, value) for key, value in response.get_json().items()])))

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
