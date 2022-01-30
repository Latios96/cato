import schedule

from cato_server.usecases.fail_timed_out_tests import FailTimedOutTests

import logging

from cato_server.authentication.remove_expired_sessions import RemoveExpiredSessions

logger = logging.getLogger(__name__)


class BackgroundTaskCreator:
    def __init__(
        self,
        fail_timed_out_tests: FailTimedOutTests,
        remove_expired_sessions: RemoveExpiredSessions,
    ):
        self._fail_timed_out_tests = fail_timed_out_tests
        self._remove_expired_sessions = remove_expired_sessions

    def create(self):
        logger.info("Creating background tasks..")

        schedule.every(2).minutes.do(self._fail_timed_out_tests.fail_timed_out_tests)
        logger.info("Created task fail_timed_out_tests.")

        schedule.every(5).minutes.do(
            self._remove_expired_sessions.remove_expired_sessions
        )
        logger.info("Created task remove_expired_sessions.")

        logger.info("Created background tasks.")
