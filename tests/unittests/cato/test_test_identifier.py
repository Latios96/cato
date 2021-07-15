import pytest

from cato_server.domain.test_identifier import TestIdentifier


def test_from_string():
    assert TestIdentifier.from_string("suite/test") == TestIdentifier("suite", "test")


def test_from_string_invalid():
    with pytest.raises(ValueError):
        assert TestIdentifier.from_string("suite/test/invalid")


def test_construct_valid():
    test_identifier = TestIdentifier("suite", "test")

    assert test_identifier.suite_name == "suite"
    assert test_identifier.test_name == "test"


@pytest.mark.parametrize(
    "suite_name,test_name",
    [
        ("test/invalid", "valid"),
        ("valid", "test/invalid"),
        ("test/invalid", "invalid/test"),
    ],
)
def test_construct_invalid(suite_name, test_name):
    with pytest.raises(ValueError):
        assert TestIdentifier(suite_name, test_name)
