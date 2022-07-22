from celery import Celery

from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.task_queue.create_thumbnail_task import (
    CreateThumbnailTask,
    CreateThumbnailParams,
)


class CatoCelery:
    def __init__(
        self,
        celery_app: Celery,
        create_thumbnail_task: CreateThumbnailTask,
        object_mapper: ObjectMapper,
    ):
        self.celery_app = celery_app
        self._object_mapper = object_mapper
        self._create_thumbnail_task = create_thumbnail_task

        @self.celery_app.task
        def _create_thumbnail(params_str: str):
            return self._create_thumbnail_task.execute(params_str)

        self._create_thumbnail_celery_task = _create_thumbnail

    def launch_create_thumbnail_task(self, test_result_id: int):
        return self._wrap_launch(
            self._create_thumbnail_celery_task,
            CreateThumbnailParams(test_result_id=test_result_id),
        )

    def _wrap_launch(self, task, params):
        params_str = self._object_mapper.to_json(params)
        return task.delay(params_str)
