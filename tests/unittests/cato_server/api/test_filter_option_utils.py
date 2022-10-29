import pytest
from starlette.datastructures import ImmutableMultiDict

from cato_common.domain.branch_name import BranchName
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_server.api.filter_option_utils import (
    result_filter_options_from_request,
    suite_result_filter_options_from_request,
    run_filter_options_from_request,
)
from cato_server.storage.abstract.run_filter_options import RunFilterOptions
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
            status=StatusFilter.NONE, failure_reason=None
        )

    def test_from_request_success_with_status_filter_not_set(self):
        request_args = ImmutableMultiDict({})

        test_result_filter_options = result_filter_options_from_request(request_args)

        assert test_result_filter_options == TestResultFilterOptions(
            status=StatusFilter.NONE, failure_reason=None
        )

    def test_from_request_success_with_failure_reason(self):
        request_args = ImmutableMultiDict(
            {"statusFilter": "FAILED", "failureReasonFilter": "TIMED_OUT"}
        )

        test_result_filter_options = result_filter_options_from_request(request_args)

        assert test_result_filter_options == TestResultFilterOptions(
            status=StatusFilter.FAILED, failure_reason=TestFailureReason.TIMED_OUT
        )

    def test_from_request_success_with_no_failure_reason_when_status_filter_is_not_failed(
        self,
    ):
        request_args = ImmutableMultiDict(
            {"statusFilter": "NONE", "failureReasonFilter": "TIMED_OUT"}
        )

        test_result_filter_options = result_filter_options_from_request(request_args)

        assert test_result_filter_options == TestResultFilterOptions(
            status=StatusFilter.NONE, failure_reason=None
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


class TestRunFilterOptionUtils:
    @pytest.mark.parametrize(
        "data,filter_options",
        [
            ({}, None),
            ({"branches": "main"}, RunFilterOptions(branches={BranchName("main")})),
            (
                {"branches": "main,dev,setup-ci"},
                RunFilterOptions(
                    branches={
                        BranchName("main"),
                        BranchName("dev"),
                        BranchName("setup-ci"),
                    }
                ),
            ),
            (
                {"branches": "main,dev,"},
                RunFilterOptions(branches={BranchName("main"), BranchName("dev")}),
            ),
            (
                {"branches": "main,  dev,"},
                RunFilterOptions(branches={BranchName("main"), BranchName("dev")}),
            ),
        ],
    )
    def test_from_request_args(self, data, filter_options):
        request_args = ImmutableMultiDict(data)

        run_filter_options = run_filter_options_from_request(request_args)

        assert run_filter_options == filter_options
