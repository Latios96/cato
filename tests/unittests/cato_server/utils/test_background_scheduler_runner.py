import time
from unittest import mock

from cato_server.utils.background_scheduler_runner import BackgroundSchedulerRunner


def test_should_start_and_stop():
    mock_scheduler = mock.MagicMock()
    task_runner = BackgroundSchedulerRunner(mock_scheduler)

    task_runner.start()
    time.sleep(1)

    mock_scheduler.run_pending.assert_called()

    task_runner.stop()

    assert mock_scheduler.run_pending.call_count <= 3
