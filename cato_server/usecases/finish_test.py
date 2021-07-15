import datetime
import logging
from typing import Optional

from cato.domain.test_status import TestStatus
from cato_api_models.catoapimodels import TestResultFinishedDto
from cato_server.configuration.optional_component import OptionalComponent
from cato_server.domain.event import Event
from cato_server.domain.execution_status import ExecutionStatus
from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.queues.abstract_message_queue import AbstractMessageQueue
from cato_server.storage.abstract.test_heartbeat_repository import (
    TestHeartbeatRepository,
)
from cato_server.storage.abstract.test_result_repository import TestResultRepository

logger = logging.getLogger(__name__)


class FinishTest:
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        test_heartbeat_repository: TestHeartbeatRepository,
        message_queue: OptionalComponent[AbstractMessageQueue],
        object_mapper: ObjectMapper,
    ):
        self._test_result_repository = test_result_repository
        self._test_heartbeat_repository = test_heartbeat_repository
        self._message_queue = message_queue
        self._object_mapper = object_mapper

    def finish_test(
        self,
        test_result_id: int,
        status: TestStatus,
        seconds: float,
        message: str,
        image_output: Optional[int] = None,
        reference_image: Optional[int] = None,
    ) -> None:
        logger.info(
            "Finishing test test with id %s and message %s", test_result_id, message
        )
        test_result = self._test_result_repository.find_by_id(test_result_id)
        if not test_result:
            raise ValueError(f"No TestResult with id {test_result_id} found!")

        test_result.execution_status = ExecutionStatus.FINISHED
        test_result.status = status
        test_result.seconds = seconds
        test_result.message = message
        test_result.image_output = image_output
        test_result.reference_image = reference_image
        test_result.finished_at = self._get_finished_time()

        test_result = self._test_result_repository.save(test_result)
        logger.info("Finished test with id %s", test_result_id)

        test_heartbeat = self._test_heartbeat_repository.find_by_test_result_id(
            test_result_id
        )
        if test_heartbeat:
            logger.info("Removing heartbeat %s", test_heartbeat)
            self._test_heartbeat_repository.delete_by_id(test_heartbeat.id)

        if self._message_queue.is_available():
            dto = TestResultFinishedDto(test_result.id)
            event = Event("TEST_RESULT_FINISHED", dto)
            logger.info("Sending event %s", event)
            self._message_queue.component.send_event(
                "test_result_events",
                str(test_result.suite_result_id),
                event,
                self._object_mapper,
            )

    def fail_test(self, test_result_id: int, message: str) -> None:
        logger.info("Failing test with id %s with message %s", test_result_id, message)
        self.finish_test(
            test_result_id=test_result_id,
            status=TestStatus.FAILED,
            seconds=-1,
            message=message,
        )
        logger.info("Failed test with id %s", test_result_id)

    def _get_finished_time(self):
        return datetime.datetime.now()
