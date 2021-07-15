from typing import Generic, TypeVar, Optional, Iterable, List

from cato_server.storage.abstract.page import PageRequest, Page

T = TypeVar("T")
K = TypeVar("K")


class AbstractRepository(Generic[T, K]):
    def save(self, entity: T) -> T:
        raise NotImplementedError()

    def insert_many(self, entities: Iterable[T]) -> List[T]:
        raise NotImplementedError()

    def find_by_id(self, id: K) -> Optional[T]:
        raise NotImplementedError()

    def find_all(self) -> List[T]:
        raise NotImplementedError()

    def find_all_with_paging(self, page_request: PageRequest) -> Page[T]:
        raise NotImplementedError()

    def delete_by_id(self, id: K) -> None:
        raise NotImplementedError()
