import pytest

from cato_common.domain.auth.api_token_id import ApiTokenId


@pytest.mark.parametrize("invalid_string", ["", "  "])
def test_create_from_invalid_string(invalid_string):
    with pytest.raises(ValueError):
        ApiTokenId(invalid_string)


def test_create_valid_api_token_id():
    ApiTokenId("api_token_id")


def test_to_str():
    api_token_id = ApiTokenId("api_token_id")

    assert str(api_token_id) == "api_token_id"


def test_api_token_ids_with_same_str_should_be_equal():
    a = ApiTokenId("api_token_id")
    b = ApiTokenId("api_token_id")

    assert a == b


def test_api_token_ids_with_different_str_should_not_be_equal():
    a = ApiTokenId("api_token_id")
    b = ApiTokenId("api_token_id_")

    assert a != b


def test_should_hash_correctly():
    assert {
        ApiTokenId("api_token_id"),
        ApiTokenId("api_token_id"),
        ApiTokenId("api_token_id_"),
    } == {
        ApiTokenId("api_token_id"),
        ApiTokenId("api_token_id_"),
    }
