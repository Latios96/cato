from cato.domain.test_identifier import TestIdentifier


def test_from_string():
    assert TestIdentifier.from_string("suite/test") == TestIdentifier("suite", "test")
