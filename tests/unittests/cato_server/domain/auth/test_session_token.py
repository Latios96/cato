import pytest

from cato_server.domain.auth.session_token import SessionToken


@pytest.mark.parametrize("invalid_string", ["", "  "])
def test_create_from_invalid_string(invalid_string):
    with pytest.raises(ValueError):
        SessionToken(invalid_string)


def test_create_valid_session_token():
    SessionToken("session_token")


def test_to_str():
    session_token = SessionToken("session_token")

    assert str(session_token) == "session_token"


def test_session_tokens_with_same_str_should_be_equal():
    a = SessionToken("session_token")
    b = SessionToken("session_token")

    assert a == b


def test_session_tokens_with_different_str_should_not_be_equal():
    a = SessionToken("session_token")
    b = SessionToken("session_token_")

    assert a != b


def test_should_hash_correctly():
    assert {
        SessionToken("session_token"),
        SessionToken("session_token"),
        SessionToken("session_token_"),
    } == {
        SessionToken("session_token"),
        SessionToken("session_token_"),
    }
