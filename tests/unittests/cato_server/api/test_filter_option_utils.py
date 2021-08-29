# does not contain
# does contain
# does contain invalid
import pytest
from starlette.datastructures import ImmutableMultiDict

from cato_server.api.filter_option_utils import result_filter_options_from_request
from cato_server.storage.abstract.test_result_filter_options import (
    TestResultFilterOptions,
    StatusFilter,
)


def test_from_request_success_with_status_filter_set():
    request_args = ImmutableMultiDict({"status_filter": "NONE"})

    test_result_filter_options = result_filter_options_from_request(request_args)

    assert test_result_filter_options == TestResultFilterOptions(
        status=StatusFilter.NONE
    )


def test_from_request_success_with_status_filter_not_set():
    request_args = ImmutableMultiDict({})

    test_result_filter_options = result_filter_options_from_request(request_args)

    assert test_result_filter_options == TestResultFilterOptions(
        status=StatusFilter.NONE
    )


def test_from_request_success_with_status_filter_invalid_value():
    request_args = ImmutableMultiDict({"status_filter": "INVALID_VALUE"})

    with pytest.raises(ValueError):
        result_filter_options_from_request(request_args)
