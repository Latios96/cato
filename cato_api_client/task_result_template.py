import datetime
import logging
from typing import TypeVar

from tenacity import stop_after_attempt, wait_fixed, before_log, after_log, retry

from cato_api_client.http_template import HttpTemplate
from cato_server.task_queue.task_result import (
    TaskResult,
    TaskResultState,
)  # todo move to cato_common

logger = logging.getLogger(__name__)

T = TypeVar("T")


class TaskResultTemplate:
    def __init__(self, http_template: HttpTemplate):
        self._http_template = http_template

    def wait_for_task_result_to_complete(
        self,
        task_result: TaskResult[T],
        timeout: datetime.timedelta,
        poll_interval: datetime.timedelta,
    ):
        @retry(
            stop=stop_after_attempt(int(timeout.total_seconds())),
            wait=wait_fixed(poll_interval.total_seconds()),
            before=before_log(logger, logging.DEBUG),
            after=after_log(logger, logging.DEBUG),
        )
        def fetch_task_result():
            task_result_response = self._http_template.get_for_entity(
                task_result.url, TaskResult
            )
            assert task_result_response.get_entity().state != TaskResultState.PENDING
            return task_result_response.get_entity()

        return fetch_task_result()
