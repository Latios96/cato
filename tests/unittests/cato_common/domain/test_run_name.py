import pytest

from cato_common.domain.run_name import RunName


@pytest.mark.parametrize("invalid_string", ["", "  "])
def test_create_from_invalid_string(invalid_string):
    with pytest.raises(ValueError):
        RunName(invalid_string)


def test_create_valid_run_name():
    RunName("mac-os")


def test_to_str():
    run_name = RunName("mac-os")

    assert str(run_name) == "mac-os"


def test_run_names_with_same_str_should_be_equal():
    a = RunName("mac-os")
    b = RunName("mac-os")

    assert a == b


def test_run_names_with_different_str_should_not_be_equal():
    a = RunName("mac-os")
    b = RunName("mac-os_")

    assert a != b


def test_should_hash_correctly():
    assert {RunName("mac-os"), RunName("mac-os"), RunName("mac-os_")} == {
        RunName("mac-os"),
        RunName("mac-os_"),
    }
