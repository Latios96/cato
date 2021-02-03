import pytest

from cato_server.storage.abstract.page import PageRequest, Page


class TestPageRequest:
    def test_create_first_page(self):
        page_request = PageRequest.first(10)

        assert PageRequest(1, 10) == page_request

    def test_offset_first_page(self):
        page_request = PageRequest.first(10)

        assert page_request.offset == 0

    def test_offset_second_page(self):
        page_request = PageRequest(2, 10)

        assert page_request.offset == 10


class TestPage:
    def test_from_page_request(self):
        page_request = PageRequest.first(10)
        entities = [1, 2, 3]

        page = Page.from_page_request(page_request, 10, entities)

        assert page == Page(1, 10, 1, entities)

    @pytest.mark.parametrize(
        "total_entity_count,total_pages",
        [(0, 1), (1, 1), (9, 1), (10, 1), (11, 2), (50, 5), (100, 10)],
    )
    def test_correct_total_page_count(self, total_entity_count, total_pages):
        page_request = PageRequest.first(10)
        entities = [1, 2, 3]

        page = Page.from_page_request(page_request, total_entity_count, entities)
        assert page == Page(1, 10, total_pages, entities)
