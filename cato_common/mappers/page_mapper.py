import json
from typing import Dict, TypeVar, Type

from cato_common.mappers.object_mapper import ObjectMapper
from cato_common.storage.page import Page

T = TypeVar("T")


class PageMapper:
    def __init__(self, object_mapper: ObjectMapper):
        self._object_mapper = object_mapper

    def to_dict(self, page: Page[T]) -> Dict:
        return {
            "pageNumber": page.page_number,
            "pageSize": page.page_size,
            "totalEntityCount": page.total_entity_count,
            "entities": self._object_mapper.many_to_dict(page.entities),
        }

    def from_dict(self, the_dict: Dict, cls: Type[T]) -> Page[T]:
        return Page(
            page_number=the_dict["pageNumber"],
            page_size=the_dict["pageSize"],
            total_entity_count=the_dict["totalEntityCount"],
            entities=self._object_mapper.many_from_dict(the_dict["entities"], cls),
        )

    def to_json(self, obj: Page[T]) -> str:
        return json.dumps(self.to_dict(obj))

    def from_json(self, json_str: str, cls: Type[T]) -> Page[T]:
        return self.from_dict(json.loads(json_str), cls)
