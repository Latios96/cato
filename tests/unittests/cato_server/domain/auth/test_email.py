import pytest

from cato_server.domain.auth.email import Email


@pytest.mark.parametrize("invalid_string", ["", "  ", "foo", "foo@bar", "@bar"])
def test_create_from_invalid_string(invalid_string):
    with pytest.raises(ValueError):
        Email(invalid_string)


def test_create_valid_email():
    Email("foo@bar.com")


def test_to_str():
    email = Email("foo@bar.com")

    assert str(email) == "foo@bar.com"


def test_emails_with_same_str_should_be_equal():
    a = Email("foo@bar.com")
    b = Email("foo@bar.com")

    assert a == b


def test_emails_with_different_str_should_not_be_equal():
    a = Email("foo@bar.com")
    b = Email("bar@bar.com")

    assert a != b


def test_should_hash_correctly():
    assert {Email("foo@bar.com"), Email("foo@bar.com"), Email("bar@bar.com")} == {
        Email("foo@bar.com"),
        Email("bar@bar.com"),
    }
