from typing import Type, TypeVar, Optional

from cato_server.mappers.abstract_class_mapper import AbstractClassMapper

T = TypeVar("T")


class MapperRegistry:
    def __init__(self):
        self._mappers = {}

    def register_mapper(self, cls: Type[T], mapper: AbstractClassMapper[T]) -> None:
        self._mappers[cls] = mapper

    def class_mapper_for_cls(self, cls: Type[T]) -> Optional[AbstractClassMapper[T]]:
        return self._mappers.get(cls)
