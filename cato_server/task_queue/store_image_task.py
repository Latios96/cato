from dataclasses import dataclass

from cato_common.dtos.store_image_result import StoreImageResult
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.images.store_image import StoreImage
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.task_queue.task import Task


@dataclass
class StoreImageParams:
    original_file_id: int


class StoreImageTask(Task):
    def __init__(
        self,
        object_mapper: ObjectMapper,
        file_storage: AbstractFileStorage,
        store_image: StoreImage,
    ):
        super(StoreImageTask, self).__init__(object_mapper, StoreImageParams)
        self._file_storage = file_storage
        self._store_image = store_image

    def _execute(self, params: StoreImageParams) -> StoreImageResult:
        original_file = self._file_storage.find_by_id(params.original_file_id)
        if not original_file:
            raise RuntimeError(
                f"Did not expect to not find a File with id {params.original_file_id} in the db.",
            )
        image = self._store_image.store_image_from_file_entity(original_file)

        return StoreImageResult(image=image)
