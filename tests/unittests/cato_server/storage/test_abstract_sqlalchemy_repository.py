from dataclasses import dataclass

import pytest
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker

from cato_common.storage.page import PageRequest, Page
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    Base,
    AbstractSqlAlchemyRepository,
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


@pytest.fixture
def sessionmaker_fixture(sqlalchemy_engine):
    Base.metadata.create_all(sqlalchemy_engine)
    return sessionmaker(bind=sqlalchemy_engine)


class TestSave:
    def test_insert_single_entity(self, sessionmaker_fixture):
        repository = ExampleRepository(sessionmaker_fixture)
        entity = ExampleClass(id=0, name="test")

        saved_entity = repository.save(entity)

        assert saved_entity.id == 1
        entity.id = 1
        assert entity == saved_entity

    def test_update_single_entity(self, sessionmaker_fixture):
        repository = ExampleRepository(sessionmaker_fixture)
        entity = repository.save(ExampleClass(id=0, name="test"))

        entity.name = "test_update"
        repository.save(entity)
        entity = repository.find_by_id(entity.id)

        assert entity.name == "test_update"

    def test_insert_many_insert_empty_list(self, sessionmaker_fixture):
        repository = ExampleRepository(sessionmaker_fixture)
        inserted_entities = repository.insert_many([])

        assert inserted_entities == []

    def test_insert_many_entities(self, sessionmaker_fixture):
        repository = ExampleRepository(sessionmaker_fixture)
        inserted_entities = repository.insert_many(
            [ExampleClass(id=0, name="test") for x in range(20)]
        )

        assert inserted_entities == [
            ExampleClass(id=x, name="test") for x in range(1, 21)
        ]


class TestFinding:
    def test_find_by_id_should_return_none_if_not_found(self, sessionmaker_fixture):
        repository = ExampleRepository(sessionmaker_fixture)

        not_found_entity = repository.find_by_id(1)

        assert not_found_entity is None

    def test_find_by_id_should_return_entity(self, sessionmaker_fixture):
        repository = ExampleRepository(sessionmaker_fixture)
        entity = repository.save(ExampleClass(id=0, name="test"))

        not_found_entity = repository.find_by_id(entity.id)

        assert not_found_entity == ExampleClass(id=1, name="test")

    def test_find_all_should_return_empty_list(self, sessionmaker_fixture):
        repository = ExampleRepository(sessionmaker_fixture)

        not_found_entities = repository.find_all()

        assert not_found_entities == []

    def test_find_all_should_return_entities(self, sessionmaker_fixture):
        repository = ExampleRepository(sessionmaker_fixture)
        repository.insert_many([ExampleClass(id=0, name="test") for x in range(20)])

        entities = repository.find_all()

        assert entities == [ExampleClass(id=x, name="test") for x in range(1, 21)]


class TestDelete:
    def test_delete_by_not_existing_id_should_raise_exception(
        self, sessionmaker_fixture
    ):
        repository = ExampleRepository(sessionmaker_fixture)

        with pytest.raises(ValueError):
            repository.delete_by_id(1)

    def test_delete_by_id_should_delete_the_single_entity(self, sessionmaker_fixture):
        repository = ExampleRepository(sessionmaker_fixture)
        repository.insert_many([ExampleClass(id=0, name="test") for x in range(20)])

        repository.delete_by_id(1)
        entities_after_delete = repository.find_all()

        assert entities_after_delete == [
            ExampleClass(id=x, name="test") for x in range(2, 21)
        ]


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
