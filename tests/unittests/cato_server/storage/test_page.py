from cato_server.storage.abstract.page import PageRequest


class TestPageRequest:
    def test_create_first_page(self):
        page_request = PageRequest.first(10)

        assert PageRequest(0, 10) == page_request
