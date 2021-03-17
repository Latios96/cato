from urllib.parse import urlparse


def format_url(url: str) -> str:
    url = url.rstrip("/")
    parsed_url = urlparse(url)

    if parsed_url.scheme and parsed_url.scheme != "http":
        raise ValueError("Invalid scheme: {}".format(parsed_url.scheme))

    path = parsed_url.path

    if not parsed_url.path and parsed_url.netloc:
        path = parsed_url.netloc

    return "{}://{}".format("http", path)
