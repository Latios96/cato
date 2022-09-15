import pytest

from cato_common.domain.run_identifier import RunIdentifier


@pytest.mark.parametrize("invalid_string", ["", "  "])
def test_create_from_invalid_string(invalid_string):
    with pytest.raises(ValueError):
        RunIdentifier(invalid_string)


def test_create_valid_run_identifier():
    RunIdentifier("3046812908-2")


def test_to_str():
    run_identifier = RunIdentifier("3046812908-2")

    assert str(run_identifier) == "3046812908-2"


def test_run_identifier_with_same_str_should_be_equal():
    a = RunIdentifier("3046812908-2")
    b = RunIdentifier("3046812908-2")

    assert a == b


def test_run_identifier_with_different_str_should_not_be_equal():
    a = RunIdentifier("3046812908-2")
    b = RunIdentifier("other")

    assert a != b


def test_should_hash_correctly():
    assert {
        RunIdentifier("3046812908-2"),
        RunIdentifier("3046812908-2"),
        RunIdentifier("other"),
    } == {
        RunIdentifier("3046812908-2"),
        RunIdentifier("other"),
    }
