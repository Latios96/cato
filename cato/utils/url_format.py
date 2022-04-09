from urllib.parse import urlparse


def format_url(url: str) -> str:
    url = url.rstrip("/")
    parsed_url = urlparse(url)

    if parsed_url.scheme and parsed_url.scheme not in {"http", "https"}:
        raise ValueError("Invalid scheme: {}".format(parsed_url.scheme))

    scheme = parsed_url.scheme
    if not parsed_url.scheme:
        scheme = "http"

    path = parsed_url.path

    if not parsed_url.path and parsed_url.netloc:
        path = parsed_url.netloc

    return "{}://{}".format(scheme, path)
