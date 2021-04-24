import datetime
import logging

from cato_server.domain.execution_status import ExecutionStatus
from cato_server.storage.abstract.test_result_repository import TestResultRepository

logger = logging.getLogger(__name__)


class StartTest:
    def __init__(
        self,
        test_result_repository: TestResultRepository,
    ):
        self._test_result_repository = test_result_repository

    def start_test(self, test_result_id: int):
        logger.info("Starting test test with id %s", test_result_id)
        test_result = self._test_result_repository.find_by_id(test_result_id)
        if not test_result:
            raise ValueError(f"No TestResult with id {test_result_id} found!")

        test_result.execution_status = ExecutionStatus.RUNNING
        test_result.started_at = datetime.datetime.now()

        test_result = self._test_result_repository.save(test_result)
        logger.info("Starting test with id %s", test_result_id)
