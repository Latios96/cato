from dataclasses import dataclass
from typing import TypeVar, Generic, List

T = TypeVar("T")


@dataclass
class PageRequest:
    page_number: int
    page_size: int

    @staticmethod
    def first(page_size: int):
        return PageRequest(0, page_size)


@dataclass
class Page(Generic[T]):
    page_number: int
    total_pages: int
    element_count: int
    items: List[T]
