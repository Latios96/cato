import copy
from dataclasses import _is_dataclass_instance, fields, is_dataclass
from typing import Type, Dict, TypeVar, Collection

from cato_server.mappers.mapper_registry import MapperRegistry

T = TypeVar("T")


class GenericClassMapper:
    def __init__(self, mapper_registry: MapperRegistry):
        self._mapper_registry = mapper_registry

    def map_from_dict(self, json_data: Dict, cls: Type[T]) -> T:
        return self._from_dict(json_data, cls)

    def map_to_dict(self, obj: T) -> Dict:
        return self._to_dict(obj)

    def _to_dict(self, obj):
        if self._mapper_registry.value_mapper_for_cls(obj.__class__):
            mapper = self._mapper_registry.value_mapper_for_cls(obj.__class__)
            return mapper.map_to(obj)
        elif self._mapper_registry.class_mapper_for_cls(obj.__class__):
            mapper = self._mapper_registry.class_mapper_for_cls(obj.__class__)
            return mapper.map_to_dict(obj)
        elif _is_dataclass_instance(obj):
            result = {}
            for field in fields(obj):
                result[field.name] = self._to_dict(getattr(obj, field.name))
            return result
        elif (
            isinstance(obj, Collection)
            and not isinstance(obj, str)
            and not isinstance(obj, bytes)
        ):
            return [self._to_dict(o) for o in obj]
        else:
            return copy.deepcopy(obj)

    def _from_dict(self, json_data, cls):
        type_hint_args = getattr(cls, "__args__", ())
        is_optional = None.__class__ in type_hint_args
        if is_optional:
            if json_data is None:
                return None
            cls = type_hint_args[0]
        else:
            if json_data is None:
                raise KeyError(f"Class {cls} is not optional, but not provided")
        if self._mapper_registry.class_mapper_for_cls(cls):
            mapper = self._mapper_registry.class_mapper_for_cls(cls)
            return mapper.map_from_dict(json_data)
        elif self._mapper_registry.value_mapper_for_cls(cls):
            mapper = self._mapper_registry.value_mapper_for_cls(cls)
            return mapper.map_from(json_data)
        elif is_dataclass(cls):
            args_dict = {}
            for field in fields(cls):
                args_dict[field.name] = self._from_dict(
                    json_data.get(field.name), field.type
                )
            return cls(**args_dict)
        elif isinstance(json_data, list):
            collection_type = cls.__args__[0]
            return [self._from_dict(o, collection_type) for o in json_data]
        else:
            return copy.deepcopy(json_data)
