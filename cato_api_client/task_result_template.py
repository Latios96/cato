import datetime
import logging
from typing import TypeVar, Type

from tenacity import (
    stop_after_attempt,
    wait_fixed,
    before_log,
    after_log,
    retry,
    retry_if_exception_type,
    RetryError,
)

from cato_api_client.http_template import HttpTemplate
from cato_common.mappers.object_mapper import ObjectMapper
from cato_common.domain.tasks.task_result import (
    TaskResult,
    TaskResultState,
)

logger = logging.getLogger(__name__)

T = TypeVar("T")


class TaskResultTemplate:
    def __init__(self, http_template: HttpTemplate, object_mapper: ObjectMapper):
        self._http_template = http_template
        self._object_mapper = object_mapper

    def wait_for_task_result_to_complete(
        self,
        task_result: TaskResult,
        result_cls: Type[T],
        timeout: datetime.timedelta,
        poll_interval: datetime.timedelta,
    ) -> T:
        @retry(
            retry=retry_if_exception_type(AssertionError),
            stop=stop_after_attempt(int(timeout.total_seconds())),
            wait=wait_fixed(poll_interval.total_seconds()),
            before=before_log(logger, logging.DEBUG),
            after=after_log(logger, logging.DEBUG),
        )
        def fetch_task_result():
            task_result_response = self._http_template.get_for_entity(
                task_result.url, TaskResult[result_cls]
            )
            if not task_result_response.status_code() == 200:
                raise ValueError(
                    f"Something went wrong when retrieving task result: {fetch_task_result}"
                )

            entity = task_result_response.get_entity()
            assert entity.state != TaskResultState.PENDING

            return self._object_mapper.from_dict(entity.result, result_cls)

        try:
            return fetch_task_result()
        except RetryError:
            raise RuntimeError(
                f"Timeout while retrieving task result {fetch_task_result}"
            )
