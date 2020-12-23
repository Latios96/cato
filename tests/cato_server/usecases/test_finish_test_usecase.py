import datetime

import pytest

from cato.domain.test_status import TestStatus
from cato_server.configuration.optional_component import OptionalComponent
from cato_server.domain.execution_status import ExecutionStatus
from cato_server.domain.test_heartbeat import TestHeartbeat
from cato_server.queues.abstract_message_queue import AbstractMessageQueue
from cato_server.storage.abstract.test_heartbeat_repository import (
    TestHeartbeatRepository,
)
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.finish_test import FinishTest
from tests.utils import mock_safe


def test_should_finish(test_result_factory):
    test_result_repository = mock_safe(TestResultRepository)
    started_at = datetime.datetime.now()
    finished_at = datetime.datetime.now()
    test_result_repository.find_by_id.return_value = test_result_factory(
        id=42, started_at=started_at
    )
    test_heartbeat_repository = mock_safe(TestHeartbeatRepository)
    test_heartbeat_repository.find_by_test_result_id.return_value = TestHeartbeat(
        id=2, test_result_id=42, last_beat=datetime.datetime.now()
    )
    message_queue = OptionalComponent(mock_safe(AbstractMessageQueue))
    finish_test = FinishTest(
        test_result_repository, test_heartbeat_repository, message_queue
    )
    finish_test._get_finished_time = lambda: finished_at

    finish_test.finish_test(
        test_result_id=42,
        status=TestStatus.SUCCESS,
        seconds=2,
        message="Test succeded",
        image_output=2,
        reference_image=3,
    )

    test_result_repository.save.assert_called_with(
        test_result_factory(
            id=42,
            execution_status=ExecutionStatus.FINISHED,
            status=TestStatus.SUCCESS,
            seconds=2,
            message="Test succeded",
            image_output=2,
            reference_image=3,
            started_at=started_at,
            finished_at=finished_at,
        )
    )
    test_heartbeat_repository.delete_by_id.assert_called_with(2)
    message_queue.component.send_event.assert_called_once()


def test_should_raise_no_test_result_with_id():
    test_result_repository = mock_safe(TestResultRepository)
    test_result_repository.find_by_id.return_value = None
    test_heartbeat_repository = mock_safe(TestHeartbeatRepository)
    test_heartbeat_repository.find_by_test_result_id.return_value = TestHeartbeat(
        id=2, test_result_id=42, last_beat=datetime.datetime.now()
    )
    message_queue = OptionalComponent(mock_safe(AbstractMessageQueue))
    finish_test = FinishTest(
        test_result_repository, test_heartbeat_repository, message_queue
    )

    with pytest.raises(ValueError):
        finish_test.finish_test(
            test_result_id=42,
            status=TestStatus.SUCCESS,
            seconds=2,
            message="Test succeded",
            image_output=2,
            reference_image=3,
        )


def test_should_fail_test(test_result_factory):
    test_result_repository = mock_safe(TestResultRepository)
    started_at = datetime.datetime.now()
    finished_at = datetime.datetime.now()
    test_result_repository.find_by_id.return_value = test_result_factory(
        id=42, started_at=started_at
    )
    test_heartbeat_repository = mock_safe(TestHeartbeatRepository)
    test_heartbeat_repository.find_by_test_result_id.return_value = TestHeartbeat(
        id=2, test_result_id=42, last_beat=datetime.datetime.now()
    )
    message_queue = OptionalComponent(mock_safe(AbstractMessageQueue))
    finish_test = FinishTest(
        test_result_repository, test_heartbeat_repository, message_queue
    )
    finish_test._get_finished_time = lambda: finished_at

    finish_test.fail_test(42, "This is a test")

    test_result_repository.save.assert_called_with(
        test_result_factory(
            id=42,
            execution_status=ExecutionStatus.FINISHED,
            status=TestStatus.FAILED,
            seconds=-1,
            message="This is a test",
            image_output=None,
            reference_image=None,
            started_at=started_at,
            finished_at=finished_at,
        )
    )
    test_heartbeat_repository.delete_by_id.assert_called_with(2)
    message_queue.component.send_event.assert_called_once()
