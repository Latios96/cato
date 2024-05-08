from celery import Celery

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.task_queue.compare_image_task import (
    CompareImageTask,
    CompareImageParams,
)
from cato_server.task_queue.create_thumbnail_task import (
    CreateThumbnailTask,
    CreateThumbnailParams,
)
from cato_server.task_queue.transcode_image_task import (
    TranscodeImageTask,
    TranscodeImageParams,
)


class CatoCelery:
    def __init__(
        self,
        celery_app: Celery,
        create_thumbnail_task: CreateThumbnailTask,
        transcode_image_task: TranscodeImageTask,
        compare_image_task: CompareImageTask,
        object_mapper: ObjectMapper,
    ):
        self.celery_app = celery_app
        self._object_mapper = object_mapper
        self._create_thumbnail_task = create_thumbnail_task
        self._transcode_image_task = transcode_image_task
        self._compare_image_task = compare_image_task

        @self.celery_app.task
        def _create_thumbnail(params_str: str):
            return self._create_thumbnail_task.execute(params_str)

        self._create_thumbnail_celery_task = _create_thumbnail

        @self.celery_app.task
        def _transcode_image(params_str: str):
            return self._transcode_image_task.execute(params_str)

        self._transcode_image_celery_task = _transcode_image

        @self.celery_app.task
        def _compare_image(params_str: str):
            return self._compare_image_task.execute(params_str)

        self._compare_image_celery_task = _compare_image

    def launch_create_thumbnail_task(self, test_result_id: int):
        return self._wrap_launch(
            self._create_thumbnail_celery_task,
            CreateThumbnailParams(test_result_id=test_result_id),
        )

    def launch_transcode_image_task(self, image_id: int):
        return self._wrap_launch(
            self._transcode_image_celery_task,
            TranscodeImageParams(image_id=image_id),
        )

    def launch_compare_image_task(
        self,
        output_image_id: int,
        reference_image_id: int,
        comparison_settings: ComparisonSettings,
    ):
        return self._wrap_launch(
            self._compare_image_celery_task,
            CompareImageParams(
                output_image_id=output_image_id,
                reference_image_id=reference_image_id,
                comparison_settings=comparison_settings,
            ),
        )

    def _wrap_launch(self, task, params):
        params_str = self._object_mapper.to_json(params)
        return task.delay(params_str)
