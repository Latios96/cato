import pytest

from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_common.domain.auth.bearer_token import BearerToken


def test_get_data_dict(fixed_api_token_str):
    assert fixed_api_token_str.data_dict() == {
        "createdAt": "2022-03-21T17:15:24.328633",
        "expiresAt": "2022-03-21T19:15:24.328633",
        "id": "ab5d20008bb1f27a1442a4da398c01712b4858d0621bef08602b76f104cef16f",
        "name": "test",
    }


def test_from_bearer_token():
    bearer_token = BearerToken("test_value")
    assert ApiTokenStr.from_bearer(bearer_token) == ApiTokenStr("test_value")


def test_to_bearer_token():
    api_token_str = ApiTokenStr("test_value")
    assert api_token_str.to_bearer() == BearerToken("test_value")


@pytest.mark.parametrize("invalid_string", ["", "  "])
def test_create_from_invalid_string(invalid_string):
    with pytest.raises(ValueError):
        ApiTokenStr(invalid_string)


def test_create_valid_api_token_str():
    ApiTokenStr("the_value")


def test_to_str():
    api_token_str = ApiTokenStr("the_value")

    assert str(api_token_str) == "the_value"


def test_to_bytes():
    api_token_str = ApiTokenStr("the_value")

    assert bytes(api_token_str) == b"the_value"


def test_api_token_strs_with_same_str_should_be_equal():
    a = ApiTokenStr("the_value")
    b = ApiTokenStr("the_value")

    assert a == b


def test_api_token_strs_with_different_str_should_not_be_equal():
    a = ApiTokenStr("the_value")
    b = ApiTokenStr("other_value")

    assert a != b


def test_should_hash_correctly():
    assert {
        ApiTokenStr("the_value"),
        ApiTokenStr("the_value"),
        ApiTokenStr("other_value"),
    } == {
        ApiTokenStr("the_value"),
        ApiTokenStr("other_value"),
    }
