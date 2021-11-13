import datetime


from cato_common.domain.execution_status import ExecutionStatus
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_server.storage.abstract.test_heartbeat_repository import (
    TestHeartbeatRepository,
)
from cato_server.storage.abstract.test_result_repository import TestResultRepository

import logging

from cato_server.usecases.finish_test import FinishTest

TESTS_TIMEOUT = datetime.timedelta(minutes=2)

logger = logging.getLogger(__name__)


class FailTimedOutTests:
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        test_heartbeat_repository: TestHeartbeatRepository,
        finish_test: FinishTest,
    ):
        self._test_result_repository = test_result_repository
        self._test_heartbeat_repository = test_heartbeat_repository
        self._finish_test = finish_test

    def fail_timed_out_tests(self):
        logger.info("Checking for timed out tests..")
        timed_out_date = datetime.datetime.now() - TESTS_TIMEOUT
        timed_out_heartbeats = (
            self._test_heartbeat_repository.find_last_beat_older_than(timed_out_date)
        )
        if timed_out_heartbeats:
            logger.info("Found %s timed out heartbeats..", timed_out_heartbeats)
        else:
            logger.info("No timed out heartbeats found.")
        for timed_out_heartbeat in timed_out_heartbeats:
            test_result = self._test_result_repository.find_by_id(
                timed_out_heartbeat.test_result_id
            )
            if test_result.unified_test_status == ExecutionStatus.RUNNING:
                self._finish_test.fail_test(
                    test_result.id, "Test timed out!", TestFailureReason.TIMED_OUT
                )
