from typing import Type, TypeVar, Optional, Dict

from cato_server.mappers.abstract_class_mapper import AbstractClassMapper
from cato_server.mappers.abstract_value_mapper import AbstractValueMapper

T = TypeVar("T")
M = TypeVar("M")


class MapperRegistry:
    def __init__(self):
        self._class_mappers: Dict[Type[T], AbstractClassMapper[T]] = {}
        self._value_mappers: Dict[Type[T], AbstractValueMapper[T, M]] = {}

    def register_class_mapper(
        self, cls: Type[T], mapper: AbstractClassMapper[T]
    ) -> None:
        self._class_mappers[cls] = mapper

    def class_mapper_for_cls(self, cls: Type[T]) -> Optional[AbstractClassMapper[T]]:
        return self._class_mappers.get(cls)

    def register_value_mapper(
        self, cls: Type[T], mapper: AbstractValueMapper[T, M]
    ) -> None:
        self._value_mappers[cls] = mapper

    def value_mapper_for_cls(self, cls: Type[T]) -> Optional[AbstractValueMapper[T, M]]:
        return self._value_mappers.get(cls)
