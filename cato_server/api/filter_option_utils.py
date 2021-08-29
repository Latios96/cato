from starlette.datastructures import ImmutableMultiDict

from cato_server.storage.abstract.test_result_filter_options import (
    TestResultFilterOptions,
)
from cato_server.storage.abstract.status_filter import StatusFilter


def result_filter_options_from_request(
    request_args: ImmutableMultiDict,
) -> TestResultFilterOptions:
    status_filter_string = request_args.get("statusFilter", StatusFilter.NONE)
    return TestResultFilterOptions(status=StatusFilter(status_filter_string))
