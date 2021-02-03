from cato_server.domain.project import Project
from cato_server.mappers.internal.page_class_mapper import PageClassMapper
from cato_server.storage.abstract.page import Page


def test_map_empty_to_dict(mapper_registry):
    page_class_mapper = PageClassMapper(mapper_registry)
    page = Page(
        page_number=1,
        page_size=10,
        total_pages=1,
        entities=[],
    )

    result = page_class_mapper.map_to_dict(page)

    assert result == {
        "entities": [],
        "page_number": 1,
        "page_size": 10,
        "total_pages": 1,
    }


def test_map_to_dict(mapper_registry):
    page_class_mapper = PageClassMapper(mapper_registry)
    page = Page(
        page_number=1,
        page_size=10,
        total_pages=1,
        entities=[Project(id=0, name="test")],
    )

    result = page_class_mapper.map_to_dict(page)

    assert result == {
        "entities": [{"id": 0, "name": "test"}],
        "page_number": 1,
        "page_size": 10,
        "total_pages": 1,
    }


def test_in_object_mapper(object_mapper):
    page = Page(
        page_number=1,
        page_size=10,
        total_pages=1,
        entities=[Project(id=0, name="test")],
    )

    result = object_mapper.to_dict(page)

    assert result == {
        "entities": [{"id": 0, "name": "test"}],
        "page_number": 1,
        "page_size": 10,
        "total_pages": 1,
    }
