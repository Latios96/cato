from typing import Generic, TypeVar, Optional

T = TypeVar("T")
K = TypeVar("K")


class AbstractRepository(Generic[T, K]):
    def save(self, entity: T) -> T:
        raise NotImplementedError()

    def find_by_id(self, id: K) -> Optional[T]:
        raise NotImplementedError()
