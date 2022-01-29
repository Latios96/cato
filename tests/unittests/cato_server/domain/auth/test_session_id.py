import pytest

from cato_server.domain.auth.session_id import SessionId


@pytest.mark.parametrize("invalid_string", ["", "  "])
def test_create_from_invalid_string(invalid_string):
    with pytest.raises(ValueError):
        SessionId(invalid_string)


def test_create_valid_session_id():
    SessionId("session_id")


def test_to_str():
    session_id = SessionId("session_id")

    assert str(session_id) == "session_id"


def test_session_ids_with_same_str_should_be_equal():
    a = SessionId("session_id")
    b = SessionId("session_id")

    assert a == b


def test_session_ids_with_different_str_should_not_be_equal():
    a = SessionId("session_id")
    b = SessionId("session_id_")

    assert a != b


def test_should_hash_correctly():
    assert {
        SessionId("session_id"),
        SessionId("session_id"),
        SessionId("session_id_"),
    } == {
        SessionId("session_id"),
        SessionId("session_id_"),
    }
