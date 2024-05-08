from dataclasses import dataclass

from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.images.store_image import StoreImage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.task_queue.task import Task, Void


@dataclass
class TranscodeImageParams:
    image_id: int


class TranscodeImageTask(Task):
    def __init__(
        self,
        object_mapper: ObjectMapper,
        image_repository: ImageRepository,
        store_image: StoreImage,
    ):
        super(TranscodeImageTask, self).__init__(object_mapper, TranscodeImageParams)
        self._image_repository = image_repository
        self._store_image = store_image

    def _execute(self, params: TranscodeImageParams) -> Void:
        image = self._image_repository.find_by_id(params.image_id)
        if not image:
            raise RuntimeError(
                f"Did not expect to not find an Image with id {params.image_id} in the db.",
            )

        self._store_image.transcode_image(image)

        return Void()
