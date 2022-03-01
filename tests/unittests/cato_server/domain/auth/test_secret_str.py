import pytest

from cato_server.domain.auth.secret_str import SecretStr


def test_create_from_empty_string_should_not_work():
    with pytest.raises(ValueError):
        SecretStr("")


def test_create_valid_secret_str():
    secret_str = SecretStr(" a secret ")

    assert secret_str.get_secret_value() == " a secret "


def test_to_str():
    secret_str = SecretStr(" a secret ")

    assert str(secret_str) == "******"


def test_secret_strs_with_same_str_should_be_equal():
    a = SecretStr("a secret")
    b = SecretStr("a secret")

    assert a == b


def test_secret_strs_with_different_str_should_not_be_equal():
    a = SecretStr("a secret")
    b = SecretStr("a secret")

    assert a == b


def test_should_hash_correctly():
    assert {
        SecretStr("a secret"),
        SecretStr("a secret"),
        SecretStr("another secret"),
    } == {
        SecretStr("a secret"),
        SecretStr("another secret"),
    }
