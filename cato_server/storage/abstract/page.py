from dataclasses import dataclass
from typing import TypeVar, Generic, List

T = TypeVar("T")


@dataclass
class PageRequest:
    page_number: int
    page_size: int

    def __post_init__(self):
        if self.page_number < 1:
            raise ValueError("page_number can not be less than 1.")

        if self.page_size < 0:
            raise ValueError("page_size can not be less than 0.")

    @staticmethod
    def first(page_size):
        # type: (int) -> PageRequest
        return PageRequest(1, page_size)

    @property
    def offset(self) -> int:
        return self.page_size * (self.page_number - 1)


@dataclass
class Page(Generic[T]):
    page_number: int
    page_size: int
    total_entity_count: int
    entities: List[T]

    def __post_init__(self):
        if self.page_number < 1:
            raise ValueError("page_number can not be less than 1.")
        if self.page_size < 0:
            raise ValueError("page_size can not be less than 0.")
        if self.total_entity_count < 0:
            raise ValueError("total_entity_count can not be less than 0.")

    @staticmethod
    def from_page_request(page_request, total_entity_count, entities):
        # type: (PageRequest,int,List[T]) -> Page
        return Page(
            page_number=page_request.page_number,
            page_size=page_request.page_size,
            total_entity_count=total_entity_count,
            entities=entities,
        )
