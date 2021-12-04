from typing import Optional

from starlette.datastructures import ImmutableMultiDict

from cato_common.domain.branch_name import BranchName
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_server.storage.abstract.run_filter_options import RunFilterOptions
from cato_server.storage.abstract.suite_result_filter_options import (
    SuiteResultFilterOptions,
)
from cato_server.storage.abstract.test_result_filter_options import (
    TestResultFilterOptions,
)
from cato_server.storage.abstract.status_filter import StatusFilter


def result_filter_options_from_request(
    request_args: ImmutableMultiDict,
) -> TestResultFilterOptions:
    status_filter_string = request_args.get("statusFilter", StatusFilter.NONE)
    status_filter = StatusFilter(status_filter_string)
    failure_reason = _parse_failure_reason(request_args, status_filter)
    return TestResultFilterOptions(status=status_filter, failure_reason=failure_reason)


def suite_result_filter_options_from_request(
    request_args: ImmutableMultiDict,
) -> SuiteResultFilterOptions:
    status_filter_string = request_args.get("statusFilter", StatusFilter.NONE)
    return SuiteResultFilterOptions(status=StatusFilter(status_filter_string))


def _parse_failure_reason(
    request_args: ImmutableMultiDict, status_filter: StatusFilter
):
    failure_reason = None
    if status_filter == StatusFilter.FAILED:
        failure_reason_filter_string = request_args.get("failureReasonFilter", None)
        if failure_reason_filter_string:
            failure_reason = TestFailureReason(failure_reason_filter_string)
    return failure_reason


def run_filter_options_from_request(
    request_args: ImmutableMultiDict,
) -> Optional[RunFilterOptions]:
    branches_str = request_args.get("branches")
    if branches_str:
        branches = {BranchName(x.strip()) for x in branches_str.split(",") if x.strip()}
        return RunFilterOptions(branches=branches)
    return None
