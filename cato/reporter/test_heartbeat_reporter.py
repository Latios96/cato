import threading
import time
from typing import Optional

from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato_server.domain.test_identifier import TestIdentifier

HEARTBEAT_INTERVAL_IN_SECONDS = 5

import logging

logger = logging.getLogger(__name__)


class TestHeartbeatReporter:
    def __init__(self, test_execution_reporter: TestExecutionReporter):
        self._test_execution_reporter = test_execution_reporter
        self._cease_continuous_run: Optional[threading.Event] = None

    def start_sending_heartbeats_for_test(
        self, test_identifier: TestIdentifier
    ) -> threading.Event:
        self._cease_continuous_run = threading.Event()

        class ScheduleThread(threading.Thread):
            @classmethod
            def run(cls):
                while not self._cease_continuous_run.is_set():
                    logger.debug("Sending heartbeat for %s", test_identifier)
                    self._test_execution_reporter.report_heartbeat(test_identifier)
                    time.sleep(HEARTBEAT_INTERVAL_IN_SECONDS)

        continuous_thread = ScheduleThread()
        continuous_thread.start()
        return self._cease_continuous_run

    def stop(self):
        self._cease_continuous_run.set()
