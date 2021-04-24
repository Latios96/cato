import datetime
import logging

from cato_api_models.catoapimodels import CreateFullRunDto
from cato_api_models.catoapimodels import RunDto, RunStatusDto
from cato_server.configuration.optional_component import OptionalComponent
from cato_server.domain.event import Event
from cato_server.domain.execution_status import ExecutionStatus
from cato_server.domain.machine_info import MachineInfo
from cato_server.domain.run import Run
from cato_server.domain.suite_result import SuiteResult
from cato_server.domain.test_identifier import TestIdentifier
from cato_server.domain.test_result import TestResult
from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.queues.abstract_message_queue import AbstractMessageQueue
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository

logger = logging.getLogger(__name__)


class CreateFullRunUsecase:
    def __init__(
        self,
        run_repository: RunRepository,
        suite_result_repository: SuiteResultRepository,
        test_result_repository: TestResultRepository,
        message_queue: OptionalComponent[AbstractMessageQueue],
        object_mapper: ObjectMapper,
    ):
        self._run_repository = run_repository
        self._suite_result_repository = suite_result_repository
        self._test_result_repository = test_result_repository
        self._message_queue = message_queue
        self._object_mapper = object_mapper

    def create_full_run(self, create_full_run_dto: CreateFullRunDto):
        run = Run(
            id=0,
            project_id=create_full_run_dto.project_id,
            started_at=datetime.datetime.now(),
        )
        run = self._run_repository.save(run)
        logger.info("Created run %s", run)
        for suite_dto in create_full_run_dto.test_suites:
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
                        execution_status=ExecutionStatus.NOT_STARTED,
                        seconds=0,
                    )
                )
            saved_tests = self._test_result_repository.insert_many(tests)
            logger.info(
                "Created %s test results for suite %s",
                len(saved_tests),
                suite_result.suite_name,
            )
        if self._message_queue.is_available():
            logger.info("Message queue is  available, sending RUN_CREATED event")
            run_dto = RunDto(
                id=run.id,
                project_id=run.id,
                started_at=run.started_at.isoformat(),
                status=RunStatusDto.NOT_STARTED,
            )
            run_created_event = Event("RUN_CREATED", run_dto)
            self._message_queue.component.send_event(
                "run_events",
                str(create_full_run_dto.project_id),
                run_created_event,
                self._object_mapper,
            )
            logger.info("Published event %s", run_created_event)
        else:
            logger.info("Not sending event, message queue is not available")

        return run
