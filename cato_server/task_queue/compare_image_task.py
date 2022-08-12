from dataclasses import dataclass

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.compare_image_result import CompareImageResult
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.images.store_image import StoreImage
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.task_queue.task import Task
from cato_server.usecases.compare_image import CompareImage


@dataclass
class CompareImageParams:
    output_image_id: int
    reference_image_id: int
    comparison_settings: ComparisonSettings


class CompareImageTask(Task):
    def __init__(
        self,
        object_mapper: ObjectMapper,
        file_storage: AbstractFileStorage,
        store_image: StoreImage,
        compare_image: CompareImage,
    ):
        super(CompareImageTask, self).__init__(object_mapper, CompareImageParams)
        self._object_mapper = object_mapper
        self._compare_image = compare_image
        self._file_storage = file_storage
        self._store_image = store_image

    def _execute(self, params: CompareImageParams) -> CompareImageResult:
        output_image_file = self._file_storage.find_by_id(params.output_image_id)
        if not output_image_file:
            raise RuntimeError(
                f"Did not expect to not find an Image with id {params.output_image_id} in the db.",
            )
        reference_image_file = self._file_storage.find_by_id(params.reference_image_id)
        if not reference_image_file:
            raise RuntimeError(
                f"Did not expect to not find an Image with id {params.reference_image_id} in the db.",
            )

        output_image = self._store_image.store_image_from_file_entity(output_image_file)
        reference_image = self._store_image.store_image_from_file_entity(
            reference_image_file
        )

        return self._compare_image.compare_image_from_db(
            output_image, reference_image, params.comparison_settings
        )
