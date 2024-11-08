import logging
from typing import Optional

from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
    LastRunInformation,
)
from cato.reporter.performance_stats_collector import PerformanceStatsCollector
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.utils.branch_detector import BranchDetector
from cato.utils.machine_info_cache import MachineInfoCache
from cato.utils.run_batch_identifier_detector import RunBatchIdentifierDetector
from cato.utils.run_information_detectors.run_information_detector import (
    RunInformationDetector,
)
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.config import RunConfig
from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.test import Test
from cato_common.domain.test_execution_result import TestExecutionResult
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.test_suite import TestSuite
from cato_common.dtos.create_full_run_dto import (
    TestForRunCreation,
    TestSuiteForRunCreation,
    CreateFullRunDto,
)
from cato_common.dtos.start_test_result_dto import StartTestResultDto

logger = logging.getLogger(__name__)


class TestExecutionDbReporter(TestExecutionReporter):
    __test__ = False

    def __init__(
        self,
        machine_info_cache: MachineInfoCache,
        cato_api_client: CatoApiClient,
        branch_detector: BranchDetector,
        run_batch_identifier_detector: RunBatchIdentifierDetector,
        run_information_detector: RunInformationDetector,
        performance_stats_collector: PerformanceStatsCollector,
    ):
        self._machine_info_cache = machine_info_cache
        self._cato_api_client = cato_api_client
        self.__run_id_value: Optional[int] = None
        self._machine_info: Optional[MachineInfo] = None
        self._branch_detector = branch_detector
        self._run_batch_identifier_detector = run_batch_identifier_detector
        self._run_information_detector = run_information_detector
        self._performance_stats_collector = performance_stats_collector

    def use_run_id(self, run_id: int) -> None:
        if not self._cato_api_client.run_id_exists(run_id):
            raise ValueError(f"No run with id {run_id} exists!")
        self._run_id = run_id

    def run_id(self) -> int:
        return self._run_id

    def start_execution(self, config: RunConfig) -> None:
        logger.info("Reporting execution start to server..")
        project = self._cato_api_client.get_project_by_name(config.project_name)
        if not project:
            logger.info(
                "No project with name %s exists, creating one..", config.project_name
            )
            project = self._cato_api_client.create_project(config.project_name)
            logger.info("Created project %s with id %s.", project.name, project.id)

        logger.info("Creating run..")

        suites = []
        for test_suite in config.suites:
            tests = []
            for test in test_suite.tests:
                tests.append(
                    TestForRunCreation(
                        test_name=test.name,
                        test_identifier=TestIdentifier(test_suite.name, test.name),
                        test_command=test.command,
                        test_variables=test.variables,
                        comparison_settings=test.comparison_settings,
                    )
                )
            suites.append(
                TestSuiteForRunCreation(
                    suite_name=test_suite.name,
                    suite_variables=test_suite.variables,
                    tests=tests,
                )
            )

        branch_name = self._branch_detector.detect_branch(config.resource_path)
        run_batch_identifier = self._run_batch_identifier_detector.detect()
        run_information = self._run_information_detector.detect()
        create_run_dto = CreateFullRunDto(
            project_id=project.id,
            run_batch_identifier=run_batch_identifier,
            test_suites=suites,
            run_information=run_information,
            branch_name=branch_name,
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
        machine_info = self._machine_info_cache.get_machine_info()
        start_test_result = StartTestResultDto(
            id=test_result.id, machine_info=machine_info
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
        with self._performance_stats_collector.collect_finish_test_timing():
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
        with self._performance_stats_collector.collect_upload_log_output_timing():
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

    def report_performance_trace(self, performance_trace_json: str) -> None:
        self._cato_api_client.upload_performance_trace(
            self._run_id, performance_trace_json
        )
