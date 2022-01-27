import pytest

from cato_server.domain.auth.username import Username


@pytest.mark.parametrize("invalid_string", ["", "  "])
def test_create_from_invalid_string(invalid_string):
    with pytest.raises(ValueError):
        Username(invalid_string)


def test_create_valid_username():
    Username("username")


def test_to_str():
    username = Username("username")

    assert str(username) == "username"


def test_usernames_with_same_str_should_be_equal():
    a = Username("username")
    b = Username("username")

    assert a == b


def test_usernames_with_different_str_should_not_be_equal():
    a = Username("username")
    b = Username("username_")

    assert a != b


def test_should_hash_correctly():
    assert {Username("username"), Username("username"), Username("username_")} == {
        Username("username"),
        Username("username_"),
    }
