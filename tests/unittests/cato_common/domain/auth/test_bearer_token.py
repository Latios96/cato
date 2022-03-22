import pytest

from cato_common.domain.auth.bearer_token import BearerToken


@pytest.mark.parametrize("invalid_string", ["", "  ", "test", "Bearerfoo"])
def test_parse_from_invalid_string(invalid_string):
    with pytest.raises(ValueError):
        BearerToken.parse_from_header(invalid_string)


@pytest.mark.parametrize("invalid_string", ["", "  "])
def test_create_from_invalid_string(invalid_string):
    with pytest.raises(ValueError):
        BearerToken(invalid_string)


def test_create_valid_bearer_token():
    BearerToken("the_value")


def test_to_str():
    bearer_token = BearerToken("the_value")

    assert str(bearer_token) == "Bearer the_value"


def test_bearer_tokens_with_same_str_should_be_equal():
    a = BearerToken("the_value")
    b = BearerToken("the_value")

    assert a == b


def test_bearer_tokens_with_different_str_should_not_be_equal():
    a = BearerToken("the_value")
    b = BearerToken("other_value")

    assert a != b


def test_should_hash_correctly():
    assert {
        BearerToken("the_value"),
        BearerToken("the_value"),
        BearerToken("other_value"),
    } == {
        BearerToken("the_value"),
        BearerToken("other_value"),
    }
