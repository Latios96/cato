import time

from cato.reporter.test_execution_reporter import TestExecutionReporter
from cato.reporter.test_heartbeat_reporter import TestHeartbeatReporter
from cato_server.domain.test_identifier import TestIdentifier
from tests.utils import mock_safe


def test_should_start_and_stop():
    mock_test_execution_reporter = mock_safe(TestExecutionReporter)
    heartbeat_reporter = TestHeartbeatReporter(mock_test_execution_reporter)

    test_identifier = TestIdentifier.from_string("SuiteName/TestName")
    heartbeat_reporter.start_sending_heartbeats_for_test(test_identifier)
    time.sleep(1)

    mock_test_execution_reporter.report_heartbeat.assert_called_with(test_identifier)

    heartbeat_reporter.stop()

    assert mock_test_execution_reporter.run_pending.call_count <= 3
