from cato_server.domain.project import Project
from cato_server.mappers.page_mapper import PageMapper
from cato_server.storage.abstract.page import Page


def test_map_empty_to_dict(object_mapper):
    page_class_mapper = PageMapper(object_mapper)
    page = Page(
        page_number=1,
        page_size=10,
        total_entity_count=1,
        entities=[],
    )

    result = page_class_mapper.to_dict(page)

    assert result == {
        "entities": [],
        "page_number": 1,
        "page_size": 10,
        "total_entity_count": 1,
    }


def test_map_to_dict(object_mapper):
    page_class_mapper = PageMapper(object_mapper)
    page = Page(
        page_number=1,
        page_size=10,
        total_entity_count=1,
        entities=[Project(id=0, name="test")],
    )

    result = page_class_mapper.to_dict(page)

    assert result == {
        "entities": [{"id": 0, "name": "test"}],
        "page_number": 1,
        "page_size": 10,
        "total_entity_count": 1,
    }


def test_map_from_dict(object_mapper):
    page_class_mapper = PageMapper(object_mapper)
    page_dict = {
        "entities": [{"id": 0, "name": "test"}],
        "page_number": 1,
        "page_size": 10,
        "total_entity_count": 1,
    }

    page = page_class_mapper.from_dict(page_dict, Project)

    assert page == Page(
        page_number=1,
        page_size=10,
        total_entity_count=1,
        entities=[Project(id=0, name="test")],
    )
