import math
from dataclasses import dataclass
from typing import TypeVar, Generic, List

T = TypeVar("T")


@dataclass
class PageRequest:
    page_number: int
    page_size: int

    @staticmethod
    def first(page_size: int):
        return PageRequest(1, page_size)

    @property
    def offset(self):
        return self.page_size * (self.page_number - 1)


@dataclass
class Page(Generic[T]):
    page_number: int
    page_size: int
    total_pages: int
    entities: List[T]

    @staticmethod
    def from_page_request(
        page_request: PageRequest, total_entity_count: int, entities: List[T]
    ):
        total_pages = math.ceil(total_entity_count / page_request.page_size)
        if total_pages == 0:
            total_pages = 1
        return Page(
            page_number=page_request.page_number,
            page_size=page_request.page_size,
            total_pages=total_pages,
            entities=entities,
        )
