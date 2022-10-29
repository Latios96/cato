import pytest

from cato_common.domain.tasks.task_result import (
    TaskResult,
    TaskResultState,
    IllegalStateError,
)


class TestAccessToResult:
    @pytest.mark.parametrize(
        "task_result",
        [
            TaskResult(
                task_id="test",
                state=TaskResultState.PENDING,
                url="/some/url",
                result_=None,
                error_message_=None,
            ),
            TaskResult(
                task_id="test",
                state=TaskResultState.FAILURE,
                url="/some/url",
                result_=None,
                error_message_="error",
            ),
        ],
    )
    def test_should_throw_if_state_is_not_success(self, task_result: TaskResult):
        with pytest.raises(IllegalStateError):
            assert task_result.result

    def test_should_return_result_for_successful_task_result(self):
        task_result = TaskResult(
            task_id="test",
            state=TaskResultState.SUCCESS,
            url="/some/url",
            result_=42,
            error_message_=None,
        )

        assert task_result.result == 42


class TestAccessToErrorMessage:
    @pytest.mark.parametrize(
        "task_result",
        [
            TaskResult(
                task_id="test",
                state=TaskResultState.PENDING,
                url="/some/url",
                result_=None,
                error_message_=None,
            ),
            TaskResult(
                task_id="test",
                state=TaskResultState.SUCCESS,
                url="/some/url",
                result_=42,
                error_message_=None,
            ),
        ],
    )
    def test_should_throw_if_state_is_not_failure(self, task_result: TaskResult):
        with pytest.raises(IllegalStateError):
            assert task_result.error_message

    def test_should_return_error_message_for_failed_task_result(self):
        task_result = TaskResult(
            task_id="test",
            state=TaskResultState.FAILURE,
            url="/some/url",
            result_=None,
            error_message_="error",
        )

        assert task_result.error_message == "error"
