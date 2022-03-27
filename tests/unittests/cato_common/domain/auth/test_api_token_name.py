import pytest

from cato_common.domain.auth.api_token_name import ApiTokenName


@pytest.mark.parametrize("invalid_string", ["", "  "])
def test_create_from_invalid_string(invalid_string):
    with pytest.raises(ValueError):
        ApiTokenName(invalid_string)


def test_create_valid_api_token_name():
    ApiTokenName("api_token_name")


def test_to_str():
    api_token_name = ApiTokenName("api_token_name")

    assert str(api_token_name) == "api_token_name"


def test_api_token_names_with_same_str_should_be_equal():
    a = ApiTokenName("api_token_name")
    b = ApiTokenName("api_token_name")

    assert a == b


def test_api_token_names_with_different_str_should_not_be_equal():
    a = ApiTokenName("api_token_name")
    b = ApiTokenName("api_token_name_")

    assert a != b


def test_should_hash_correctly():
    assert {
        ApiTokenName("api_token_name"),
        ApiTokenName("api_token_name"),
        ApiTokenName("api_token_name_"),
    } == {
        ApiTokenName("api_token_name"),
        ApiTokenName("api_token_name_"),
    }
