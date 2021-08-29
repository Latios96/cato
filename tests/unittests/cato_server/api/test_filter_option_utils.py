# does not contain
# does contain
# does contain invalid
import pytest
from starlette.datastructures import ImmutableMultiDict

from cato_server.api.filter_option_utils import (
    result_filter_options_from_request,
    suite_result_filter_options_from_request,
)
from cato_server.storage.abstract.suite_result_filter_options import (
    SuiteResultFilterOptions,
)
from cato_server.storage.abstract.test_result_filter_options import (
    TestResultFilterOptions,
)
from cato_server.storage.abstract.status_filter import StatusFilter


class TestTestResultFilterOptions:
    def test_from_request_success_with_status_filter_set(self):
        request_args = ImmutableMultiDict({"statusFilter": "NONE"})

        test_result_filter_options = result_filter_options_from_request(request_args)

        assert test_result_filter_options == TestResultFilterOptions(
            status=StatusFilter.NONE
        )

    def test_from_request_success_with_status_filter_not_set(self):
        request_args = ImmutableMultiDict({})

        test_result_filter_options = result_filter_options_from_request(request_args)

        assert test_result_filter_options == TestResultFilterOptions(
            status=StatusFilter.NONE
        )

    def test_from_request_success_with_status_filter_invalid_value(self):
        request_args = ImmutableMultiDict({"statusFilter": "INVALID_VALUE"})

        with pytest.raises(ValueError):
            result_filter_options_from_request(request_args)


class TestSuiteTestResultFilterOptions:
    def test_from_request_success_with_status_filter_set(self):
        request_args = ImmutableMultiDict({"statusFilter": "NONE"})

        test_result_filter_options = suite_result_filter_options_from_request(
            request_args
        )

        assert test_result_filter_options == SuiteResultFilterOptions(
            status=StatusFilter.NONE
        )

    def test_from_request_success_with_status_filter_not_set(self):
        request_args = ImmutableMultiDict({})

        test_result_filter_options = suite_result_filter_options_from_request(
            request_args
        )

        assert test_result_filter_options == SuiteResultFilterOptions(
            status=StatusFilter.NONE
        )

    def test_from_request_success_with_status_filter_invalid_value(self):
        request_args = ImmutableMultiDict({"statusFilter": "INVALID_VALUE"})

        with pytest.raises(ValueError):
            suite_result_filter_options_from_request(request_args)
