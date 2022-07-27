import json
from typing import TypeVar

from celery.result import AsyncResult

from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.configuration.app_configuration import AppConfiguration
from cato_common.domain.tasks.task_result import TaskResult, TaskResultState

T = TypeVar("T")

CELERY_STATES_FOR_PENDING = frozenset({"PENDING", "RECEIVED", "STARTED", "RETRY"})
CELERY_STATES_FOR_SUCCESS = frozenset({"SUCCESS"})
CELERY_STATES_FOR_FAILURE = frozenset({"FAILURE", "REVOKED", "REJECTED", "IGNORED"})


class TaskResultFactory:
    def __init__(
        self, app_configuration: AppConfiguration, object_mapper: ObjectMapper
    ):
        self._app_configuration = app_configuration
        self._object_mapper = object_mapper

    def from_async_result(self, async_result: AsyncResult):
        if async_result.state in CELERY_STATES_FOR_PENDING:
            return self.create_pending_result(async_result.task_id)
        elif async_result.state in CELERY_STATES_FOR_SUCCESS:
            return self.create_success_result(
                async_result.task_id, json.loads(async_result.result)
            )
        elif async_result.state in CELERY_STATES_FOR_FAILURE:
            return self.create_failed_result(
                async_result.task_id,
                self._error_message_from_traceback(async_result.traceback),
            )

    def create_pending_result(self, task_id: str) -> TaskResult:
        return TaskResult(
            task_id=task_id,
            state=TaskResultState.PENDING,
            url=self._create_url(task_id),
            result_=None,
            error_message_=None,
        )

    def create_success_result(self, task_id: str, result: T) -> TaskResult[T]:
        return TaskResult(
            task_id=task_id,
            state=TaskResultState.SUCCESS,
            url=self._create_url(task_id),
            result_=result,
            error_message_=None,
        )

    def create_failed_result(self, task_id: str, error_message: str) -> TaskResult:
        return TaskResult(
            task_id=task_id,
            state=TaskResultState.FAILURE,
            url=self._create_url(task_id),
            result_=None,
            error_message_=error_message,
        )

    def _create_url(self, task_id: str):
        return self._app_configuration.public_url + f"/api/v1/task_results/{task_id}"

    def _error_message_from_traceback(self, traceback):
        if traceback:
            return list(filter(lambda x: x, traceback.split("\n")))[-1]
        return "<no message>"
