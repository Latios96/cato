import copy
import json
from dataclasses import _is_dataclass_instance, fields, is_dataclass
from enum import Enum
from typing import Type, Dict, TypeVar, Collection

from conjure_python_client import ConjureBeanType, ConjureEncoder, ConjureDecoder

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
            and not isinstance(obj, dict)
        ):
            return [self._to_dict(o) for o in obj]
        elif issubclass(obj.__class__, ConjureBeanType):
            return json.loads(ConjureEncoder().encode(obj))
        elif isinstance(obj, Enum):
            return obj.value
        else:
            return copy.deepcopy(obj)

    def _from_dict(self, json_data, cls, name=""):
        type_hint_args = getattr(cls, "__args__", ())
        is_optional = None.__class__ in type_hint_args
        if is_optional:
            if json_data is None:
                return None
            cls = type_hint_args[0]
        else:
            if json_data is None:
                if cls == int or cls == float:
                    return 0
                raise KeyError(
                    f"Class {cls}{' for field with name '+name if name else ''} is not optional, but not provided"
                )
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
                    json_data.get(field.name), field.type, field.name
                )
            return cls(**args_dict)
        elif isinstance(json_data, list):
            collection_type = cls.__args__[0]
            return [self._from_dict(o, collection_type) for o in json_data]
        elif self._is_subclass(cls, ConjureBeanType):
            return ConjureDecoder().decode(json_data, cls)
        elif self._is_subclass(cls, Enum):
            return cls(json_data)
        else:
            return copy.deepcopy(json_data)

    def _is_subclass(self, cls, ConjureBeanType):
        try:
            return issubclass(cls, ConjureBeanType)
        except TypeError:
            return False
