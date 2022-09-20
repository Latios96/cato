import logging

from cato_common.domain.branch_name import BranchName
from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.run import Run
from cato_common.domain.run_information import OS, LocalComputerRunInformation
from cato_common.domain.suite_result import SuiteResult
from cato_common.domain.test_result import TestResult
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.dtos.create_full_run_dto import CreateFullRunDto
from cato_common.mappers.object_mapper import ObjectMapper
from cato_common.utils.datetime_utils import aware_now_in_utc
from cato_server.domain.run_batch import RunBatch
from cato_server.storage.abstract.run_batch_repository import RunBatchRepository
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)

logger = logging.getLogger(__name__)
DEFAULT_BRANCH = BranchName("default")


class CreateRunUsecase:
    def __init__(
        self,
        run_repository: RunRepository,
        run_batch_repository: RunBatchRepository,
        suite_result_repository: SuiteResultRepository,
        test_result_repository: TestResultRepository,
        object_mapper: ObjectMapper,
    ):
        self._run_repository = run_repository
        self._run_batch_repository = run_batch_repository
        self._suite_result_repository = suite_result_repository
        self._test_result_repository = test_result_repository
        self._object_mapper = object_mapper

    def create_run(self, create_run_dto: CreateFullRunDto) -> Run:
        branch_name = self._get_branch_name(create_run_dto)
        previous_run_id = self._get_previous_run_id(branch_name, create_run_dto)
        run_batch = self._get_run_batch(create_run_dto)
        local_computer_run_information = self._get_local_computer_run_information(
            create_run_dto
        )

        run = Run(
            id=0,
            project_id=create_run_dto.project_id,
            run_batch_id=run_batch.id,
            started_at=aware_now_in_utc(),
            branch_name=branch_name,
            previous_run_id=previous_run_id,
            run_information=local_computer_run_information,
        )
        run = self._run_repository.save(run)
        logger.info("Created run %s", run)
        for suite_dto in create_run_dto.test_suites:
            suite_result = SuiteResult(
                id=0,
                run_id=run.id,
                suite_name=suite_dto.suite_name,
                suite_variables=suite_dto.suite_variables,
            )
            suite_result = self._suite_result_repository.save(suite_result)
            logger.info("Created suite %s", suite_result)
            tests = []
            for test_dto in suite_dto.tests:
                tests.append(
                    TestResult(
                        id=0,
                        suite_result_id=suite_result.id,
                        test_name=test_dto.test_name,
                        test_identifier=test_dto.test_identifier,
                        test_command=test_dto.test_command,
                        test_variables=test_dto.test_variables,
                        unified_test_status=UnifiedTestStatus.NOT_STARTED,
                        seconds=0,
                        comparison_settings=ComparisonSettings(
                            method=ComparisonMethod(
                                test_dto.comparison_settings.method.value
                            ),
                            threshold=test_dto.comparison_settings.threshold,
                        ),
                        failure_reason=None,
                    )
                )
            saved_tests = self._test_result_repository.insert_many(tests)
            logger.info(
                "Created %s test results for suite %s",
                len(saved_tests),
                suite_result.suite_name,
            )

        return run

    def _get_branch_name(self, create_run_dto):
        branch_name = (
            create_run_dto.branch_name if create_run_dto.branch_name else DEFAULT_BRANCH
        )
        return branch_name

    def _get_previous_run_id(self, branch_name, create_run_dto):
        previous_run_id = None
        previous_run = self._run_repository.find_last_run_for_project(
            create_run_dto.project_id, branch_name
        )
        if previous_run:
            previous_run_id = previous_run.id
        return previous_run_id

    def _get_run_batch(self, create_run_dto: CreateFullRunDto) -> RunBatch:
        return self._run_batch_repository.find_or_save_by_project_id_and_run_batch_identifier(
            create_run_dto.project_id,
            create_run_dto.run_batch_identifier,
            lambda: RunBatch(
                id=0,
                run_batch_identifier=create_run_dto.run_batch_identifier,
                project_id=create_run_dto.project_id,
                runs=[],
            ),
        )

    def _get_local_computer_run_information(self, create_run_dto):
        return LocalComputerRunInformation(
            id=0,
            run_id=0,
            os=OS.WINDOWS,
            computer_name="unknown",
            local_username="unknown-user",
        )
