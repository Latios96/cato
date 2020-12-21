import schedule

from cato_server.usecases.fail_timed_out_tests import FailTimedOutTests

import logging

logger = logging.getLogger(__name__)


class BackgroundTaskCreator:
    def __init__(self, fail_timed_out_tests: FailTimedOutTests):
        self._fail_timed_out_tests = fail_timed_out_tests

    def create(self):
        logger.info("Creating background tasks..")

        schedule.every(2).minutes.do(self._fail_timed_out_tests.fail_timed_out_tests)
        logger.info("Created task fail_timed_out_tests..")

        logger.info("Created background tasks.")
