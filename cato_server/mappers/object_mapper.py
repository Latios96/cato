import json
from typing import TypeVar, Dict, Type, Iterable, Optional

from conjure_python_client import ConjureBeanType, ConjureDecoder, ConjureEncoder

from cato_server.mappers.abstract_class_mapper import AbstractClassMapper
from cato_server.mappers.mapper_registry import MapperRegistry

T = TypeVar("T")


class ConjureClassMapper(AbstractClassMapper[T]):
    def __init__(self, conjure_type: Type[T]):
        self._conjure_type = conjure_type

    def map_from_dict(self, json_data: Dict) -> T:
        return ConjureDecoder().decode(json_data, self._conjure_type)

    def map_to_dict(self, test_result: T) -> Dict:
        return json.loads(ConjureEncoder().encode(test_result))


class NoMapperFoundException(Exception):
    def __init__(self, cls):
        super(NoMapperFoundException, self).__init__(f"No mapper found for cls {cls}")


class ObjectMapper:
    def __init__(self, mapper_registry: MapperRegistry):
        self._mapper_registry = mapper_registry

    def to_dict(self, obj: T) -> Dict:
        mapper = self._mapper_for_cls(obj.__class__)
        if not mapper:
            raise NoMapperFoundException(obj.__class__)
        return mapper.map_to_dict(obj)

    def from_dict(self, the_dict: Dict, cls: Type[T]) -> T:
        mapper = self._mapper_for_cls(cls)
        if not mapper:
            raise NoMapperFoundException(cls)
        return mapper.map_from_dict(the_dict)

    def to_json(self, obj: T) -> str:
        return json.dumps(self.to_dict(obj))

    def from_json(self, json_str: str, cls: Type[T]) -> T:
        return self.from_dict(json.loads(json_str), cls)

    def many_to_dict(self, objs: Iterable[T]) -> Iterable[T]:
        return list(map(self.to_dict, objs))

    def many_to_json(self, objs: Iterable[T]) -> str:
        return json.dumps(self.many_to_dict(objs))

    def many_from_dict(self, the_dicts: Iterable[Dict], cls: Type[T]) -> Iterable[T]:
        return list(map(lambda x: self.from_dict(x, cls), the_dicts))

    def many_from_json(self, json_str: str, cls: Type[T]) -> Iterable[T]:
        the_dicts = json.loads(json_str)
        return self.many_from_dict(the_dicts, cls)

    def _mapper_for_cls(self, cls: Type[T]) -> Optional[AbstractClassMapper[T]]:
        if issubclass(cls, ConjureBeanType):
            return ConjureClassMapper(cls)
        return self._mapper_registry.class_mapper_for_cls(cls)
