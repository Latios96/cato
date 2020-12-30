from typing import Dict

from cato_server.mappers.abstract_class_mapper import AbstractClassMapper
from cato_server.domain.file import File


class FileClassMapper(AbstractClassMapper[File]):
    def map_from_dict(self, json_data: Dict) -> File:
        return File(
            id=json_data["id"],
            name=json_data["name"],
            hash=json_data["hash"],
            value_counter=json_data["value_counter"],
        )

    def map_to_dict(self, the_file: File) -> Dict:
        return {
            "id": the_file.id,
            "name": the_file.name,
            "hash": the_file.hash,
            "value_counter": the_file.value_counter,
        }
