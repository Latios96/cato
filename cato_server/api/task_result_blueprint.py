import logging

from celery.result import AsyncResult
from fastapi import APIRouter
from starlette.responses import JSONResponse

from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.task_queue.cato_celery import CatoCelery
from cato_server.task_queue.task_result_factory import TaskResultFactory

logger = logging.getLogger(__name__)


class TaskResultBlueprint(APIRouter):
    def __init__(
        self,
        cato_celery: CatoCelery,
        object_mapper: ObjectMapper,
        task_result_factory: TaskResultFactory,
    ):
        super(TaskResultBlueprint, self).__init__()
        self._cato_celery = cato_celery
        self._object_mapper = object_mapper
        self._task_result_factory = task_result_factory

        self.get("/result/{task_id}")(self.get_task_result)

    def get_task_result(self, task_id):
        async_result = AsyncResult(task_id, app=self._cato_celery.celery_app)
        task_result = self._task_result_factory.from_async_result(async_result)
        return JSONResponse(content=self._object_mapper.to_dict(task_result))
