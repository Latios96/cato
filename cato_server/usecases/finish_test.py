import logging
from typing import Optional

from cato_common.domain.result_status import ResultStatus
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.test_heartbeat_repository import (
    TestHeartbeatRepository,
)
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.task_queue.cato_celery import CatoCelery
from cato_common.utils.datetime_utils import aware_now_in_utc

logger = logging.getLogger(__name__)


class FinishTest:
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        test_heartbeat_repository: TestHeartbeatRepository,
        object_mapper: ObjectMapper,
        cato_celery: CatoCelery,
    ):
        self._test_result_repository = test_result_repository
        self._test_heartbeat_repository = test_heartbeat_repository
        self._object_mapper = object_mapper
        self._cato_celery = cato_celery

    def finish_test(
        self,
        test_result_id: int,
        status: ResultStatus,
        seconds: float,
        message: str,
        image_output: Optional[int] = None,
        reference_image: Optional[int] = None,
        diff_image: Optional[int] = None,
        error_value: Optional[float] = None,
        failure_reason: Optional[TestFailureReason] = None,
    ) -> None:
        logger.info(
            'Finishing test test with id %s and message "%s"', test_result_id, message
        )
        test_result = self._test_result_repository.find_by_id(test_result_id)
        if not test_result:
            raise ValueError(f"No TestResult with id {test_result_id} found!")

        test_result.unified_test_status = UnifiedTestStatus(status.value)
        test_result.seconds = seconds
        test_result.message = message
        test_result.image_output = image_output
        test_result.reference_image = reference_image
        test_result.diff_image = diff_image
        test_result.finished_at = self._get_finished_time()
        test_result.error_value = error_value
        test_result.failure_reason = failure_reason

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
                self._cato_celery.launch_create_thumbnail_task(test_result.id)
            except Exception as e:
                logger.error(
                    "Error when launching thumbnail task for test result with id %s, test result won't have a thumbnail:",
                    test_result_id,
                )
                logger.exception(e)

    def fail_test(
        self, test_result_id: int, message: str, failure_reason: TestFailureReason
    ) -> None:
        logger.info("Failing test with id %s with message %s", test_result_id, message)
        self.finish_test(
            test_result_id=test_result_id,
            status=ResultStatus.FAILED,
            seconds=-1,
            message=message,
            error_value=None,
            failure_reason=failure_reason,
        )
        logger.info("Failed test with id %s", test_result_id)

    def _get_finished_time(self):
        return aware_now_in_utc()
