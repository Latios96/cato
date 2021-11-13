import datetime
import logging

from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings
from cato_api_models.catoapimodels import CreateFullRunDto
from cato_common.domain.run import Run
from cato_common.domain.suite_result import SuiteResult
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.test_result import TestResult
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)

logger = logging.getLogger(__name__)


class CreateRunUsecase:
    def __init__(
        self,
        run_repository: RunRepository,
        suite_result_repository: SuiteResultRepository,
        test_result_repository: TestResultRepository,
        object_mapper: ObjectMapper,
    ):
        self._run_repository = run_repository
        self._suite_result_repository = suite_result_repository
        self._test_result_repository = test_result_repository
        self._object_mapper = object_mapper

    def create_run(self, create_run_dto: CreateFullRunDto) -> None:
        run = Run(
            id=0,
            project_id=create_run_dto.project_id,
            started_at=datetime.datetime.now(),
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
                        test_identifier=TestIdentifier.from_string(
                            test_dto.test_identifier
                        ),
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
