import pytest
from sqlalchemy.exc import IntegrityError

from cato_server.domain.auth_user import AuthUser
from cato_server.storage.sqlalchemy.sqlalchemy_auth_user_repository import (
    SqlAlchemyAuthUserRepository,
)


def test_save(sessionmaker_fixture):
    repository = SqlAlchemyAuthUserRepository(sessionmaker_fixture)
    auth_user = AuthUser(
        id=0, username="someuser", hashed_password="the_hashed_password"
    )

    saved_auth_user = repository.save(auth_user)

    auth_user.id = 1
    assert saved_auth_user == auth_user


@pytest.mark.parametrize(
    "auth_user",
    [
        AuthUser(id=0, username=None, hashed_password="the_hashed_password"),
        AuthUser(id=0, username="someuser", hashed_password=None),
    ],
)
def test_without_username_or_hash_should_fail(sessionmaker_fixture, auth_user):
    repository = SqlAlchemyAuthUserRepository(sessionmaker_fixture)

    with pytest.raises(IntegrityError):
        repository.save(auth_user)


def test_inserting_same_username_twice_should_fail(sessionmaker_fixture):
    repository = SqlAlchemyAuthUserRepository(sessionmaker_fixture)
    auth_user = AuthUser(
        id=0, username="someuser", hashed_password="the_hashed_password"
    )
    repository.save(auth_user)

    with pytest.raises(IntegrityError):
        repository.save(auth_user)


def test_find_by_username_should_return_existing_user(sessionmaker_fixture):
    repository = SqlAlchemyAuthUserRepository(sessionmaker_fixture)
    auth_user = AuthUser(
        id=0, username="someuser", hashed_password="the_hashed_password"
    )
    auth_user = repository.save(auth_user)

    found_user = repository.find_by_username("someuser")

    assert found_user == auth_user


def test_find_by_username_should_return_none_for_not_existing_user(
    sessionmaker_fixture,
):
    repository = SqlAlchemyAuthUserRepository(sessionmaker_fixture)

    found_user = repository.find_by_username("someuser")

    assert found_user is None
