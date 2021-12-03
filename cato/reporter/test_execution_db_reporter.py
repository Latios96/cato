import logging
from typing import List, Optional

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
from cato_api_models.catoapimodels import (
    CreateFullRunDto,
    TestSuiteForRunCreation,
    TestForRunCreation,
    StartTestResultDto,
    MachineInfoDto,
    ComparisonSettingsDto,
    ComparisonMethodDto,
)
from cato_common.domain.branch_name import BranchName
from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.test_identifier import TestIdentifier

logger = logging.getLogger(__name__)


class TestExecutionDbReporter(TestExecutionReporter):
    def __init__(
        self,
        machine_info_collector: MachineInfoCollector,
        cato_api_client: CatoApiClient,
    ):
        self._machine_info_collector = machine_info_collector
        self._cato_api_client = cato_api_client
        self.__run_id_value: Optional[int] = None
        self._machine_info: Optional[MachineInfo] = None

    def use_run_id(self, run_id: int) -> None:
        if not self._cato_api_client.run_id_exists(run_id):
            raise ValueError(f"No run with id {run_id} exists!")
        self._run_id = run_id

    def run_id(self) -> int:
        return self._run_id

    def start_execution(self, project_name: str, test_suites: List[TestSuite]) -> None:
        logger.info("Reporting execution start to server..")
        project = self._cato_api_client.get_project_by_name(project_name)
        if not project:
            logger.info("No project with name %s exists, creating one..", project_name)
            project = self._cato_api_client.create_project(project_name)
            logger.info("Created project %s", project)

        logger.info("Creating run..")

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
                        comparison_settings=ComparisonSettingsDto(
                            method=ComparisonMethodDto(test.comparison_settings.method),
                            threshold=test.comparison_settings.threshold,
                        ),
                    )
                )
            suites.append(
                TestSuiteForRunCreation(
                    suite_name=test_suite.name,
                    suite_variables=test_suite.variables,
                    tests=tests,
                )
            )

        create_run_dto = CreateFullRunDto(
            project_id=project.id, test_suites=suites, branch_name=BranchName("default")
        )
        suite_count = len(suites)
        test_count = sum(map(lambda x: len(x.tests), suites))
        logger.info(
            "Reporting execution of %s suite%s and %s test%s",
            suite_count,
            "s" if suite_count > 1 else "",
            test_count,
            "s" if test_count > 1 else "",
        )
        run = self._cato_api_client.create_run(create_run_dto)
        logger.debug("Created run %s", run)
        self._run_id = run.id
        logger.info(
            "You can find your run at %s",
            self._cato_api_client.generate_run_url(project.id, run.id),
        )

    def report_test_execution_start(self, current_suite: TestSuite, test: Test) -> None:
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

        logger.debug(f"Reporting execution start of test {test_identifier}..")
        machine_info = self._get_machine_info()
        machine_info_dto = MachineInfoDto(
            cpu_name=machine_info.cpu_name,
            cores=machine_info.cores,
            memory=machine_info.memory,
        )
        start_test_result = StartTestResultDto(
            id=test_result.id, machine_info=machine_info_dto
        )
        self._cato_api_client.start_test(start_test_result)

    def report_test_result(
        self, current_suite: TestSuite, test_execution_result: TestExecutionResult
    ) -> None:
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

        logger.info(f"Reporting test result of test {test_identifier}..")
        self._cato_api_client.finish_test(
            test_result.id,
            error_value=test_execution_result.error_value,
            status=test_execution_result.status,
            seconds=test_execution_result.seconds,
            message=test_execution_result.message,
            image_output=test_execution_result.image_output,
            reference_image=test_execution_result.reference_image,
            diff_image=test_execution_result.diff_image,
            failure_reason=test_execution_result.failure_reason,
        )

        logger.info(f"Uploading output of test {test_identifier}..")
        self._cato_api_client.upload_output(
            test_result.id, "".join(test_execution_result.output)
        )

    def report_heartbeat(self, test_identifier: TestIdentifier) -> None:
        self._cato_api_client.heartbeat_test(self._run_id, test_identifier)

    def report_test_execution_end(
        self, last_run_information_repository: LastRunInformationRepository
    ) -> None:
        last_run_id = LastRunInformation(last_run_id=self._run_id)
        last_run_information_repository.write_last_run_information(last_run_id)

    @property
    def _run_id(self) -> int:
        if self.__run_id_value is None:
            raise RuntimeError("run_id has to be set first!")
        return self.__run_id_value

    @_run_id.setter
    def _run_id(self, run_id: int) -> None:
        self.__run_id_value = run_id

    def _get_machine_info(self) -> MachineInfo:
        if not self._machine_info:
            logger.info("Collecting machine info..")
            self._machine_info = self._machine_info_collector.collect()
        return self._machine_info
