from dataclasses import dataclass
from typing import Generic, TypeVar, Type

from cato_common.mappers.object_mapper import ObjectMapper

P = TypeVar("P")
R = TypeVar("R")


class Task(Generic[P, R]):
    def __init__(self, object_mapper: ObjectMapper, params_cls: Type[P]):
        self._object_mapper = object_mapper
        self._params_cls = params_cls

    def execute(self, params_str: str) -> str:
        params = self._object_mapper.from_json(params_str, self._params_cls)
        result = self._execute(params)
        return self._object_mapper.to_json(result)

    def _execute(self, params: P) -> R:
        raise NotImplementedError()


@dataclass
class Void:
    pass
