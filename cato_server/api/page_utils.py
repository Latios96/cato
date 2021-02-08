from typing import Optional, Dict

from cato_server.storage.abstract.page import PageRequest


def page_request_from_request(flask_request_args: Dict) -> Optional[PageRequest]:
    page_number = flask_request_args.get("page_number")
    page_size = flask_request_args.get("page_size")

    if page_number is None and page_size is None:
        return None

    page_number = max(1, int(page_number))
    page_size = max(1, int(page_size))
    return PageRequest(page_number=page_number, page_size=page_size)