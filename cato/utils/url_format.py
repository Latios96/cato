from typing import cast

from url_normalize import url_normalize  # type: ignore


def format_url(url: str) -> str:
    return cast(str, url_normalize(url, default_scheme="http")[:-1])
