import pytest

from cato.utils.url_format import format_url


@pytest.mark.parametrize(
    "url,expected_url",
    [
        ("localhost:5000", "http://localhost:5000"),
        ("localhost", "http://localhost"),
        ("http://localhost", "http://localhost"),
        ("http://localhost/", "http://localhost"),
        ("http://localhost:5000", "http://localhost:5000"),
        ("http://localhost:5000/", "http://localhost:5000"),
        ("http://somename:5000", "http://somename:5000"),
        ("http://127.0.0.1:5000", "http://127.0.0.1:5000"),
        ("http://186.248.26.26:5000", "http://186.248.26.26:5000"),
        ("http://186.248.26.26", "http://186.248.26.26"),
        ("http://186.248.26.26/", "http://186.248.26.26"),
        ("http://www.github.com/", "http://www.github.com"),
        ("https://www.github.com/", "https://www.github.com"),
    ],
)
def test_url_format(url, expected_url):
    assert format_url(url) == expected_url

    assert format(expected_url) == expected_url
