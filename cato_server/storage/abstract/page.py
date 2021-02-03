import math
from typing import TypeVar, Generic, List

import attr

T = TypeVar("T")


@attr.s
class PageRequest:
    page_number: int = attr.ib()
    page_size: int = attr.ib()

    @page_number.validator
    def validate_page_number(self, attribute, value):
        if value < 1:
            raise ValueError("page_number can not be less than 1.")

    @page_size.validator
    def validate_page_size(self, attribute, value):
        if value < 0:
            raise ValueError("page_size can not be less than 0.")

    @staticmethod
    def first(page_size: int):
        return PageRequest(1, page_size)

    @property
    def offset(self):
        return self.page_size * (self.page_number - 1)


@attr.s
class Page(Generic[T]):
    page_number: int = attr.ib()
    page_size: int = attr.ib()
    total_pages: int = attr.ib()
    entities: List[T] = attr.ib()

    @page_number.validator
    def validate_page_number(self, attribute, value):
        if value < 1:
            raise ValueError("page_number can not be less than 1.")

    @page_size.validator
    def validate_page_size(self, attribute, value):
        if value < 0:
            raise ValueError("page_size can not be less than 0.")

    @total_pages.validator
    def validate_total_pages(self, attribute, value):
        if value < 1:
            raise ValueError("total_pages can not be less than 1.")

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
