from typing import Dict

from cato_server.domain.image import Image
from cato_server.mappers.abstract_class_mapper import AbstractClassMapper
from cato_server.mappers.image_channel_class_mapper import ImageChannelClassMapper


class ImageClassMapper(AbstractClassMapper[Image]):
    def map_from_dict(self, json_data: Dict) -> Image:
        return Image(
            id=json_data["id"],
            name=json_data["name"],
            original_file_id=json_data["original_file_id"],
            channels=list(
                map(
                    lambda x: ImageChannelClassMapper().map_from_dict(x),
                    json_data["channels"],
                )
            ),
            width=json_data["width"],
            height=json_data["height"],
        )

    def map_to_dict(self, the_file: Image) -> Dict:
        return {
            "id": the_file.id,
            "name": the_file.name,
            "original_file_id": the_file.original_file_id,
            "channels": list(
                map(
                    lambda x: ImageChannelClassMapper().map_to_dict(x),
                    the_file.channels,
                )
            ),
            "width": the_file.width,
            "height": the_file.height,
        }
