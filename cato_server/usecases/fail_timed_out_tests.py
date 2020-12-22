import datetime

from cato.domain.test_status import TestStatus
from cato_server.domain.execution_status import ExecutionStatus
from cato_server.storage.abstract.test_heartbeat_repository import (
    TestHeartbeatRepository,
)
from cato_server.storage.abstract.test_result_repository import TestResultRepository

import logging

TESTS_TIMEOUT = datetime.timedelta(minutes=2)

logger = logging.getLogger(__name__)


class FailTimedOutTests:
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        test_heartbeat_repository: TestHeartbeatRepository,
    ):

        self._test_result_repository = test_result_repository
        self._test_heartbeat_repository = test_heartbeat_repository

    def fail_timed_out_tests(self):
        logger.info("Checking for timed out tests..")
        timed_out_date = datetime.datetime.now() - TESTS_TIMEOUT
        timed_out_heartbeats = (
            self._test_heartbeat_repository.find_last_beat_older_than(timed_out_date)
        )
        if timed_out_heartbeats:
            logger.info(
                "Found %s timed out tests, failing them..", timed_out_heartbeats
            )
        else:
            logger.info("No timed out tests found.")
        for timed_out_heartbeat in timed_out_heartbeats:
            test_result = self._test_result_repository.find_by_id(
                timed_out_heartbeat.test_result_id
            )
            if test_result.execution_status == ExecutionStatus.RUNNING:
                test_result.execution_status = ExecutionStatus.FINISHED
                test_result.status = TestStatus.FAILED
                self._test_result_repository.save(test_result)
                logger.info(
                    "Failed test with id %s, last heartbeat was %s",
                    timed_out_heartbeat.test_result_id,
                    timed_out_heartbeat.last_beat,
                )
            logger.info("Removing timed out heartbeat %s", timed_out_heartbeat)
            self._test_heartbeat_repository.delete_by_id(timed_out_heartbeat.id)
