from starlette.datastructures import ImmutableMultiDict

from cato_server.storage.abstract.test_result_filter_options import (
    StatusFilter,
    TestResultFilterOptions,
)


def result_filter_options_from_request(
    request_args: ImmutableMultiDict,
) -> TestResultFilterOptions:
    status_filter_string = request_args.get(
        "statusFilter", StatusFilter.NONE
    )  # todo instead of None make this optional
    return TestResultFilterOptions(status=StatusFilter(status_filter_string))
