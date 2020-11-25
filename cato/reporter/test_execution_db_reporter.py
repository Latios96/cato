import datetime
import logging
from typing import List, Optional

from cato.domain.project import Project
from cato.domain.run import Run
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_suite import TestSuite
from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato.storage.abstract.abstract_test_result_repository import TestResultRepository
from cato.storage.abstract.project_repository import ProjectRepository
from cato.storage.abstract.run_repository import RunRepository
from cato.storage.abstract.suite_result_repository import SuiteResultRepository
from cato.storage.domain.execution_status import ExecutionStatus
from cato.storage.domain.suite_result import SuiteResult
from cato.storage.domain.test_result import TestResult

logger = logging.getLogger(__name__)


class TestExecutionDbReporter(TestExecutionReporter):
    def __init__(
        self,
        project_repository: ProjectRepository,
        run_repository: RunRepository,
        suite_result_repository: SuiteResultRepository,
        test_result_repository: TestResultRepository,
        file_storage: AbstractFileStorage,
    ):
        self._test_result_repository = test_result_repository
        self._suite_result_repository = suite_result_repository
        self._run_repository = run_repository
        self._project_repository = project_repository
        self._file_storage = file_storage
        self._run_id: Optional[int] = None

    def start_execution(self, project_name: str, test_suites: List[TestSuite]):
        logger.info("Reporting execution start to db..")
        project = self._project_repository.find_by_name(project_name)
        if not project:
            logger.info("No project with name %s exists, creating one..", project_name)
            project = self._project_repository.save(Project(id=0, name=project_name))
            logger.info("Created project %s", project)
        run = Run(id=0, project_id=project.id, started_at=datetime.datetime.now())
        run = self._run_repository.save(run)
        self._run_id = run.id

        for test_suite in test_suites:
            suite_result = SuiteResult(
                id=0,
                run_id=run.id,
                suite_name=test_suite.name,
                suite_variables=test_suite.variables,
            )
            suite_result = self._suite_result_repository.save(suite_result)

            for test in test_suite.tests:
                test_result = TestResult(
                    id=0,
                    suite_result_id=suite_result.id,
                    test_name=test.name,
                    test_identifier=TestIdentifier(test_suite.name, test.name),
                    test_variables=test.variables,
                    test_command=test.command,
                )
                logger.info(
                    f"Reporting execution of test {test_suite.name}/{test_result.test_name}.."
                )
                self._test_result_repository.save(test_result)

    def report_test_execution_start(self, current_suite: TestSuite, test: Test):
        suite_result = self._suite_result_repository.find_by_run_id_and_name(
            self._run_id, current_suite.name
        )
        test_identifier = TestIdentifier(current_suite.name, test.name)
        test_result = (
            self._test_result_repository.find_by_suite_result_and_test_identifier(
                suite_result.id, test_identifier
            )
        )

        test_result.execution_status = ExecutionStatus.RUNNING
        test_result.started_at = datetime.datetime.now()

        logger.info(f"Reporting execution start of test {test_identifier}..")
        self._test_result_repository.save(test_result)

    def report_test_result(
        self, current_suite: TestSuite, test_execution_result: TestExecutionResult
    ):
        suite_result = self._suite_result_repository.find_by_run_id_and_name(
            self._run_id, current_suite.name
        )
        test_identifier = TestIdentifier(
            current_suite.name, test_execution_result.test.name
        )
        test_result = (
            self._test_result_repository.find_by_suite_result_and_test_identifier(
                suite_result.id,
                test_identifier,
            )
        )
        if not test_result:
            logger.error(
                "Did not found a TestResult for suite with id %s and TestIdentifier %s",
                suite_result.id,
                test_identifier,
            )

        test_result.execution_status = ExecutionStatus.FINISHED
        test_result.finished_at = datetime.datetime.now()
        test_result.output = test_execution_result.output
        test_result.status = test_execution_result.status
        test_result.seconds = test_execution_result.seconds
        test_result.message = test_execution_result.message

        if test_execution_result.image_output:
            test_result.image_output = self._copy_to_storage(
                test_execution_result.image_output
            )
        if test_execution_result.reference_image:
            test_result.reference_image = self._copy_to_storage(
                test_execution_result.reference_image
            )

        logger.info(f"Reporting test result of test {test_identifier}..")
        self._test_result_repository.save(test_result)

    def _copy_to_storage(self, image_path: str) -> int:
        logger.info("Copy image %s to file storage..", image_path)
        return self._file_storage.save_file(image_path).id
