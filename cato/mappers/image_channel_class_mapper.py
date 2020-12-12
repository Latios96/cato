from typing import Dict

from cato.domain.image import ImageChannel
from cato.mappers.abstract_class_mapper import AbstractClassMapper


class ImageChannelClassMapper(AbstractClassMapper[ImageChannel]):
    def map_from_dict(self, json_data: Dict) -> ImageChannel:
        return ImageChannel(
            id=json_data["id"],
            image_id=json_data["image_id"],
            name=json_data["name"],
            file_id=json_data["file_id"],
        )

    def map_to_dict(self, test_result: ImageChannel) -> Dict:
        return {
            "id": test_result.id,
            "image_id": test_result.image_id,
            "name": test_result.name,
            "file_id": test_result.file_id,
        }
