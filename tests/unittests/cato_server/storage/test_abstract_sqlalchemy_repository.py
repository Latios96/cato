from dataclasses import dataclass

import pytest
from sqlalchemy import Column, Integer, String

from cato_server.storage.abstract.page import PageRequest, Page
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    Base,
    AbstractSqlAlchemyRepository,
    E,
    T,
)


@dataclass
class ExampleClass:
    id: int
    name: str


class ExampleMapping(Base):
    __tablename__ = "example_mapping_entity"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)


class ExampleRepository(
    AbstractSqlAlchemyRepository[ExampleClass, ExampleMapping, int]
):
    def to_entity(self, domain_object: ExampleClass) -> ExampleMapping:
        return ExampleMapping(
            id=domain_object.id if domain_object.id else None, name=domain_object.name
        )

    def to_domain_object(self, entity: ExampleMapping) -> ExampleClass:
        return ExampleClass(id=entity.id, name=entity.name)

    def mapping_cls(self):
        return ExampleMapping


class TestPaging:
    def test_find_all_with_paging_first_page_page_is_empty(self, sessionmaker_fixture):
        repository = ExampleRepository(sessionmaker_fixture)
        page_request = PageRequest.first(20)

        page = repository.find_all_with_paging(page_request)

        assert page == Page.from_page_request(page_request, 0, [])

    @pytest.mark.parametrize(
        "total_entity_count,page, on_page",
        [
            (0, 1, [0, 0]),
            (1, 1, [1, 1]),
            (9, 1, [1, 9]),
            (10, 1, [1, 10]),
            (11, 1, [1, 10]),
            (11, 2, [11, 11]),
            (50, 1, [1, 10]),
            (50, 2, [11, 20]),
            (50, 3, [21, 30]),
            (100, 1, [1, 10]),
        ],
    )
    def test_find_all_with_paging_first_page_page(
        self, total_entity_count, page, on_page, sessionmaker_fixture
    ):
        repository = ExampleRepository(sessionmaker_fixture)
        repository.insert_many(
            [ExampleClass(id=0, name="test") for x in range(total_entity_count)]
        )
        page_request = PageRequest(page, 10)

        page = repository.find_all_with_paging(page_request)

        assert page == Page.from_page_request(
            page_request,
            total_entity_count,
            [
                ExampleClass(id=x, name="test")
                for x in range(on_page[0], on_page[1] + 1 if on_page[1] else 0)
            ],
        )
