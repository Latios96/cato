import datetime
from dataclasses import dataclass
from typing import Dict, Type, TypeVar

import pytest

from cato_api_client.http_template import HttpTemplate, HttpTemplateResponse
from cato_api_client.task_result_template import TaskResultTemplate
from cato_server.task_queue.task_result import TaskResult, TaskResultState


from tests.utils import mock_safe

R = TypeVar("R")

SUCCESSFUL_TASK_RESULT = {
    "taskId": "id",
    "state": TaskResultState.SUCCESS,
    "url": "/test",
    "result_": {"value": 42},
    "errorMessage_": None,
}

PENDING_TASK_RESULT = {
    "taskId": "id",
    "state": TaskResultState.PENDING,
    "url": "/test",
    "result_": None,
    "errorMessage_": None,
}


@pytest.fixture
def test_context(object_mapper):
    class TestContext:
        def __init__(self):
            self.mock_http_template = mock_safe(HttpTemplate)
            self.task_result_template = TaskResultTemplate(
                self.mock_http_template, object_mapper
            )

    return TestContext()


@pytest.fixture()
def mock_http_template_response_factory(object_mapper):
    class Response:
        def __init__(self, status_code, json_value):
            self.status_code = status_code
            self._json_value = json_value

        def json(self):
            return self._json_value

    def mock_http_template_response(
        status_code: int, json_value: Dict, response_cls: Type[R]
    ):
        return HttpTemplateResponse(
            Response(status_code, json_value), response_cls, object_mapper
        )

    return mock_http_template_response


@dataclass
class MyResult:
    value: int


def test_should_get_task_result_successfully(
    test_context, mock_http_template_response_factory
):
    task_result_to_wait_for = TaskResult(
        task_id="id",
        state=TaskResultState.PENDING,
        url="/test",
        result_=None,
        error_message_=None,
    )

    response_1 = mock_http_template_response_factory(
        200,
        PENDING_TASK_RESULT,
        TaskResult,
    )
    response_2 = mock_http_template_response_factory(
        200,
        PENDING_TASK_RESULT,
        TaskResult,
    )
    response_3 = mock_http_template_response_factory(
        200,
        SUCCESSFUL_TASK_RESULT,
        TaskResult,
    )
    test_context.mock_http_template.get_for_entity.side_effect = [
        response_1,
        response_2,
        response_3,
    ]

    result = test_context.task_result_template.wait_for_task_result_to_complete(
        task_result_to_wait_for,
        MyResult,
        timeout=datetime.timedelta(seconds=10),
        poll_interval=datetime.timedelta(seconds=0.5),
    )

    assert result.value == 42


def test_should_timeout(test_context, mock_http_template_response_factory):
    task_result_to_wait_for = TaskResult(
        task_id="id",
        state=TaskResultState.PENDING,
        url="/test",
        result_=None,
        error_message_=None,
    )

    response_1 = mock_http_template_response_factory(
        200,
        PENDING_TASK_RESULT,
        TaskResult,
    )
    test_context.mock_http_template.get_for_entity.side_effect = [
        response_1,
    ]

    with pytest.raises(RuntimeError):
        test_context.task_result_template.wait_for_task_result_to_complete(
            task_result_to_wait_for,
            MyResult,
            timeout=datetime.timedelta(seconds=0.1),
            poll_interval=datetime.timedelta(seconds=0.5),
        )


def test_should_throw_when_requests_does_not_return_200(
    test_context, mock_http_template_response_factory
):
    task_result_to_wait_for = TaskResult(
        task_id="id",
        state=TaskResultState.PENDING,
        url="/test",
        result_=None,
        error_message_=None,
    )

    response_1 = mock_http_template_response_factory(
        500,
        PENDING_TASK_RESULT,
        TaskResult,
    )

    test_context.mock_http_template.get_for_entity.side_effect = [response_1]

    with pytest.raises(ValueError):
        test_context.task_result_template.wait_for_task_result_to_complete(
            task_result_to_wait_for,
            MyResult,
            timeout=datetime.timedelta(seconds=10),
            poll_interval=datetime.timedelta(seconds=0.5),
        )
