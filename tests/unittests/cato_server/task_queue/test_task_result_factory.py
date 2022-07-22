import uuid

import pytest
from celery.result import AsyncResult

from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.task_queue.task_result import TaskResult, TaskResultState
from cato_server.task_queue.task_result_factory import TaskResultFactory
from tests.utils import mock_safe

TASK_ID = str(uuid.uuid4())
TASK_URL = f"http://127.0.0.1/api/v1/task_results/{TASK_ID}"

REAL_TRACEBACK = """Traceback (most recent call last):
  File "C:\Python37\Lib\code.py", line 90, in runcode
    exec(code, self.locals)
  File "<input>", line 1, in <module>
ValueError: Test"""


@pytest.fixture
def task_result_factory(object_mapper):
    return TaskResultFactory(AppConfigurationDefaults().create(), object_mapper)


def test_should_create_pending_task_result(task_result_factory):
    pending_result = task_result_factory.create_pending_result(TASK_ID)

    assert pending_result == TaskResult(
        task_id=TASK_ID,
        state=TaskResultState.PENDING,
        url=TASK_URL,
        _result=None,
        _error_message=None,
    )


def test_should_create_successful_task_result(task_result_factory):
    successful_result = task_result_factory.create_success_result(TASK_ID, 42)

    assert successful_result == TaskResult(
        task_id=TASK_ID,
        state=TaskResultState.SUCCESS,
        url=TASK_URL,
        _result=42,
        _error_message=None,
    )


def test_should_create_failed_task_result(task_result_factory):
    failed_result = task_result_factory.create_failed_result(
        TASK_ID, "this is my error message"
    )

    assert failed_result == TaskResult(
        task_id=TASK_ID,
        state=TaskResultState.FAILURE,
        url=TASK_URL,
        _result=None,
        _error_message="this is my error message",
    )


class TestFromAsyncResult:
    @pytest.mark.parametrize(
        "celery_status", ["PENDING", "RECEIVED", "STARTED", "RETRY"]
    )
    def test_should_create_pending_task_result(
        self, celery_status, task_result_factory
    ):
        async_result = mock_safe(AsyncResult)
        async_result.task_id = TASK_ID
        async_result.state = celery_status

        pending_result = task_result_factory.from_async_result(async_result)

        assert pending_result == TaskResult(
            task_id=TASK_ID,
            state=TaskResultState.PENDING,
            url=TASK_URL,
            _result=None,
            _error_message=None,
        )

    def test_should_create_successful_task_result(self, task_result_factory):
        async_result = mock_safe(AsyncResult)
        async_result.task_id = TASK_ID
        async_result.state = "SUCCESS"
        async_result.result = '{"value": 42}'

        successful_result = task_result_factory.from_async_result(async_result)

        assert successful_result == TaskResult(
            task_id=TASK_ID,
            state=TaskResultState.SUCCESS,
            url=TASK_URL,
            _result={"value": 42},
            _error_message=None,
        )

    @pytest.mark.parametrize(
        "traceback, expected_message",
        [
            (REAL_TRACEBACK, "ValueError: Test"),
            ("", "<no message>"),
            ("ValueError", "ValueError"),
        ],
    )
    @pytest.mark.parametrize(
        "celery_status", ["FAILURE", "REVOKED", "REJECTED", "IGNORED"]
    )
    def test_should_create_failed_task_result(
        self, celery_status, traceback, expected_message, task_result_factory
    ):
        async_result = mock_safe(AsyncResult)
        async_result.task_id = TASK_ID
        async_result.state = "FAILURE"
        async_result.traceback = traceback

        failed_result = task_result_factory.from_async_result(async_result)

        assert failed_result == TaskResult(
            task_id=TASK_ID,
            state=TaskResultState.FAILURE,
            url=TASK_URL,
            _result=None,
            _error_message=expected_message,
        )
