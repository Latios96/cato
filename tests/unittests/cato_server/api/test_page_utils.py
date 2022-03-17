import pytest

from cato_server.api.page_utils import page_request_from_request
from cato_common.storage.page import PageRequest


@pytest.mark.parametrize(
    "data,page_request",
    [
        ({}, None),
        ({"pageSize": 0, "pageNumber": 0}, PageRequest(1, 1)),
        ({"pageSize": -1, "pageNumber": -1}, PageRequest(1, 1)),
        ({"pageSize": 3, "pageNumber": 2}, PageRequest(2, 3)),
    ],
)
def test_page_request_from_request(data, page_request):
    assert page_request_from_request(data) == page_request
