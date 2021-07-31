import copy
import datetime
from dataclasses import _is_dataclass_instance, fields
from enum import Enum
from typing import Type, Dict, TypeVar, Mapping, Collection

import attr
from dataclasses_json.core import (
    _decode_dataclass,
    _encode_overrides,
    _user_overrides_or_exts,
)
from dataclasses_json.utils import _handle_undefined_parameters_safe

from cato_server.mappers.abstract_class_mapper import AbstractClassMapper
from cato_server.mappers.mapper_registry import MapperRegistry

T = TypeVar("T")


class GenericClassMapper(AbstractClassMapper[T]):
    def __init__(self, mapper_registry: MapperRegistry):
        self._mapper_registry = mapper_registry

    def map_from_dict(self, json_data: Dict) -> T:
        pass

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
