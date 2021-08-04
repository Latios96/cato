import json
from typing import TypeVar, Dict, Type, Iterable, List

from cato_server.mappers.generic_class_mapper import GenericClassMapper
from cato_server.storage.abstract.page import Page

T = TypeVar("T")


class ObjectMapper:
    def __init__(self, generic_class_mapper: GenericClassMapper):
        self._generic_class_mapper = generic_class_mapper

    def to_dict(self, obj: T) -> Dict:
        if isinstance(obj, dict):
            return obj
        if isinstance(obj, Page):
            raise RuntimeError(
                "ObjectMapper can not map Page instances, use PageMapper instead!"
            )
        return self._generic_class_mapper.map_to_dict(obj)

    def from_dict(self, the_dict: Dict, cls: Type[T]) -> T:
        return self._generic_class_mapper.map_from_dict(the_dict, cls)

    def to_json(self, obj: T) -> str:
        return json.dumps(self.to_dict(obj))

    def from_json(self, json_str: str, cls: Type[T]) -> T:
        return self.from_dict(json.loads(json_str), cls)

    def many_to_dict(self, objs: Iterable[T]) -> List[T]:
        return list(map(self.to_dict, objs))

    def many_to_json(self, objs: Iterable[T]) -> str:
        return json.dumps(self.many_to_dict(objs))

    def many_from_dict(self, the_dicts: Iterable[Dict], cls: Type[T]) -> List[T]:
        return list(map(lambda x: self.from_dict(x, cls), the_dicts))

    def many_from_json(self, json_str: str, cls: Type[T]) -> List[T]:
        the_dicts = json.loads(json_str)
        return self.many_from_dict(the_dicts, cls)
