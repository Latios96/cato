import pytest

from cato_server.api.page_utils import page_request_from_request
from cato_common.storage.page import PageRequest


@pytest.mark.parametrize(
    "data,page_request",
    [
        ({}, None),
        ({"page_size": 0, "page_number": 0}, PageRequest(1, 1)),
        ({"page_size": -1, "page_number": -1}, PageRequest(1, 1)),
        ({"page_size": 3, "page_number": 2}, PageRequest(2, 3)),
    ],
)
def test_page_request_from_request(data, page_request):
    assert page_request_from_request(data) == page_request
