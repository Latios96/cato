from typing import TypeVar, Generic, Optional

T = TypeVar("T")
M = TypeVar("M")


class AbstractValueMapper(Generic[T, M]):
    def map_from(self, json_data: Optional[M]) -> Optional[T]:
        raise NotImplementedError()

    def map_to(self, test_result: T) -> M:
        raise NotImplementedError()
