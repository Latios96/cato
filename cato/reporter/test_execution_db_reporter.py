import datetime
import logging

from typing import List

from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_suite import TestSuite
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
    LastRunInformation,
)
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.utils.machine_info_collector import MachineInfoCollector
from cato_api_client.cato_api_client import CatoApiClient
from cato_api_models._impl import catoapimodels_MachineInfoDto
from cato_api_models.catoapimodels import (
    CreateFullRunDto,
    TestSuiteForRunCreation,
    TestForRunCreation,
)
from cato_server.domain.execution_status import ExecutionStatus
from cato_server.domain.run import Run
from cato_server.domain.test_identifier import TestIdentifier

logger = logging.getLogger(__name__)


class TestExecutionDbReporter(TestExecutionReporter):
    def __init__(
        self,
        machine_info_collector: MachineInfoCollector,
        cato_api_client: CatoApiClient,
    ):
        self._machine_info_collector = machine_info_collector
        self._cato_api_client = cato_api_client
        self._run_id = None

    def use_run_id(self, run_id: int):
        if not self._cato_api_client.run_id_exists(run_id):
            raise ValueError(f"No run with id {run_id} exists!")
        self._run_id = run_id

    def start_execution(self, project_name: str, test_suites: List[TestSuite]):
        logger.info("Reporting execution start to server..")
        project = self._cato_api_client.get_project_by_name(project_name)
        if not project:
            logger.info("No project with name %s exists, creating one..", project_name)
            project = self._cato_api_client.create_project(project_name)
            logger.info("Created project %s", project)

        logger.info("Creating run..")
        run = Run(id=0, project_id=project.id, started_at=datetime.datetime.now())
        run = self._cato_api_client.create_run(run)
        self._run_id = run.id

        logger.info("Collecting machine info..")
        machine_info = self._machine_info_collector.collect()
        machine_info_dto = catoapimodels_MachineInfoDto(
            cpu_name=machine_info.cpu_name,
            cores=machine_info.cores,
            memory=machine_info.memory,
        )

        suites = []
        for test_suite in test_suites:
            tests = []
            for test in test_suite.tests:
                tests.append(
                    TestForRunCreation(
                        test_name=test.name,
                        test_identifier=str(TestIdentifier(test_suite.name, test.name)),
                        test_command=test.command,
                        test_variables=test.variables,
                        machine_info=machine_info_dto,
                    )
                )
            suites.append(
                TestSuiteForRunCreation(
                    suite_name=test_suite.name,
                    suite_variables=test_suite.variables,
                    tests=tests,
                )
            )

        create_full_run_dto = CreateFullRunDto(
            project_id=project.id, test_suites=suites
        )
        logger.info("Reporting execution of %s suites", len(suites))
        run = self._cato_api_client.create_full_run(create_full_run_dto)
        logger.debug("Created run %s", run)
        self._run_id = run.id
        logger.info(
            "You can find your run at %s",
            self._cato_api_client.generate_run_url(project.id, run.id),
        )

    def report_test_execution_start(self, current_suite: TestSuite, test: Test):
        test_identifier = TestIdentifier(current_suite.name, test.name)
        test_result = self._cato_api_client.find_test_result_by_run_id_and_identifier(
            self._run_id, test_identifier
        )
        if test_result is None:
            logger.error(
                "Did not found a TestResult for suite with run id %s and TestIdentifier %s",
                self._run_id,
                test_identifier,
            )
            return

        test_result.execution_status = ExecutionStatus.RUNNING
        test_result.started_at = datetime.datetime.now()

        logger.debug(f"Reporting execution start of test {test_identifier}..")
        self._cato_api_client.update_test_result(test_result)

    def report_test_result(
        self, current_suite: TestSuite, test_execution_result: TestExecutionResult
    ):
        test_identifier = TestIdentifier(
            current_suite.name, test_execution_result.test.name
        )

        test_result = self._cato_api_client.find_test_result_by_run_id_and_identifier(
            self._run_id, test_identifier
        )

        if test_result is None:
            logger.error(
                "Did not found a TestResult for suite with run id %s and TestIdentifier %s",
                self._run_id,
                test_identifier,
            )
            return

        image_output_id = None
        if test_execution_result.image_output:
            image_output_id = self._cato_api_client.upload_image(
                test_execution_result.image_output
            ).id
        reference_image_id = None
        if test_execution_result.reference_image:
            reference_image_id = self._cato_api_client.upload_image(
                test_execution_result.reference_image
            ).id

        logger.info(f"Reporting test result of test {test_identifier}..")
        self._cato_api_client.finish_test(
            test_result.id,
            status=test_execution_result.status,
            seconds=test_execution_result.seconds,
            message=test_execution_result.message,
            image_output=image_output_id,
            reference_image=reference_image_id,
        )

        logger.info(f"Uploading output of test {test_identifier}..")
        self._cato_api_client.upload_output(
            test_result.id, "".join(test_execution_result.output)
        )

    def report_heartbeat(self, test_identifier: TestIdentifier):
        self._cato_api_client.heartbeat_test(self._run_id, test_identifier)

    def report_test_execution_end(
        self, last_run_information_repository: LastRunInformationRepository
    ):
        last_run_id = LastRunInformation(last_run_id=self._run_id)
        last_run_information_repository.write_last_run_information(last_run_id)

    @property
    def _run_id(self) -> int:
        if self.__run_id_value is None:
            raise RuntimeError("run_id has to be set first!")
        return self.__run_id_value

    @_run_id.setter
    def _run_id(self, run_id: int):
        self.__run_id_value = run_id
