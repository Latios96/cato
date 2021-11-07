import datetime
import logging
from typing import Optional

from cato.domain.test_status import TestStatus
from cato_common.domain.execution_status import ExecutionStatus
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.test_heartbeat_repository import (
    TestHeartbeatRepository,
)
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.create_thumbnail import CreateThumbnail

logger = logging.getLogger(__name__)


class FinishTest:
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        test_heartbeat_repository: TestHeartbeatRepository,
        object_mapper: ObjectMapper,
        create_thumbnail: CreateThumbnail,
    ):
        self._test_result_repository = test_result_repository
        self._test_heartbeat_repository = test_heartbeat_repository
        self._object_mapper = object_mapper
        self._create_thumbnail = create_thumbnail

    def finish_test(
        self,
        test_result_id: int,
        status: TestStatus,
        seconds: float,
        message: str,
        image_output: Optional[int] = None,
        reference_image: Optional[int] = None,
        diff_image: Optional[int] = None,
        error_value: Optional[float] = None,
    ) -> None:
        logger.info(
            'Finishing test test with id %s and message "%s"', test_result_id, message
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
        test_result.diff_image = diff_image
        test_result.finished_at = self._get_finished_time()
        test_result.error_value = error_value

        test_result = self._test_result_repository.save(test_result)
        logger.info("Finished test with id %s", test_result_id)

        test_heartbeat = self._test_heartbeat_repository.find_by_test_result_id(
            test_result_id
        )
        if test_heartbeat:
            logger.info("Removing heartbeat %s", test_heartbeat)
            self._test_heartbeat_repository.delete_by_id(test_heartbeat.id)

        if test_result.reference_image or test_result.image_output:
            try:
                self._create_thumbnail.create_thumbnail(test_result)
            except Exception as e:
                logger.error(
                    "Error when creating thumbnail for test result with id %s, test result won't have a thumbnail:",
                    test_result_id,
                )
                logger.exception(e)

    def fail_test(self, test_result_id: int, message: str) -> None:
        logger.info("Failing test with id %s with message %s", test_result_id, message)
        self.finish_test(
            test_result_id=test_result_id,
            status=TestStatus.FAILED,
            seconds=-1,
            message=message,
            error_value=None,
        )
        logger.info("Failed test with id %s", test_result_id)

    def _get_finished_time(self):
        return datetime.datetime.now()
