import json
from typing import Dict, TypeVar, Type

from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.page import Page

T = TypeVar("T")


class PageMapper:
    def __init__(self, object_mapper: ObjectMapper):
        self._object_mapper = object_mapper

    def to_dict(self, page: Page[T]) -> Dict:
        return {
            "page_number": page.page_number,
            "page_size": page.page_size,
            "total_pages": page.total_pages,
            "entities": self._object_mapper.many_to_dict(page.entities),
        }

    def from_dict(self, the_dict: Dict, cls: Type[T]) -> Page[T]:
        return Page(
            page_number=the_dict["page_number"],
            page_size=the_dict["page_size"],
            total_pages=the_dict["total_pages"],
            entities=self._object_mapper.many_from_dict(the_dict["entities"], cls),
        )

    def to_json(self, obj: T) -> str:
        return json.dumps(self.to_dict(obj))

    def from_json(self, json_str: str, cls: Type[T]) -> Page[T]:
        return self.from_dict(json.loads(json_str), cls)
