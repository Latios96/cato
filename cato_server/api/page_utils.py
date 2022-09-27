from typing import Optional

from starlette.datastructures import ImmutableMultiDict

from cato_common.storage.page import PageRequest


def page_request_from_request(
    request_args: ImmutableMultiDict,
) -> Optional[PageRequest]:
    page_number = request_args.get("pageNumber")
    page_size = request_args.get("pageSize")

    if page_number is None or page_size is None:
        return None
    try:
        page_number = max(1, int(page_number))
        page_size = max(1, int(page_size))
        return PageRequest(page_number=page_number, page_size=page_size)
    except ValueError:
        return None
