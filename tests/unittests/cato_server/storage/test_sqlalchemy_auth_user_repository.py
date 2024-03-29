import pytest
from sqlalchemy.exc import IntegrityError

from cato_server.domain.auth.auth_user import AuthUser
from cato_common.domain.auth.email import Email
from cato_common.domain.auth.username import Username
from cato_server.storage.sqlalchemy.sqlalchemy_auth_user_repository import (
    SqlAlchemyAuthUserRepository,
    _AuthUserMapping,
)


def test_save(sqlalchemy_auth_user_repository):
    auth_user = AuthUser(
        id=0,
        username=Username("someuser"),
        fullname=Username("User Userson"),
        email=Email("foo@bar.com"),
    )

    saved_auth_user = sqlalchemy_auth_user_repository.save(auth_user)

    auth_user.id = 1
    assert saved_auth_user == auth_user


class TestSchemaConstraints:
    @pytest.mark.parametrize(
        "auth_user_mapping",
        [
            _AuthUserMapping(
                id=None, username=None, fullname="User Username", email="foo@bar.com"
            ),
            _AuthUserMapping(
                id=None, username="someuser", fullname=None, email="foo@bar.com"
            ),
            _AuthUserMapping(
                id=None, username="someuser", fullname="User Username", email=None
            ),
        ],
    )
    def test_without_username_fullname_or_email_should_fail(
        self, auth_user_mapping, sessionmaker_fixture
    ):
        session = sessionmaker_fixture()

        with pytest.raises(IntegrityError):
            session.add(auth_user_mapping)
            session.commit()

    def test_inserting_same_username_twice_should_fail(
        self, sqlalchemy_auth_user_repository
    ):
        auth_user = AuthUser(
            id=0,
            username=Username("someuser"),
            fullname=Username("User Userson"),
            email=Email("foo@bar.com"),
        )
        sqlalchemy_auth_user_repository.save(auth_user)

        with pytest.raises(IntegrityError):
            sqlalchemy_auth_user_repository.save(auth_user)

    def test_inserting_same_username_different_casing_twice_should_fail(
        self, sqlalchemy_auth_user_repository
    ):
        auth_user = AuthUser(
            id=0,
            username=Username("someuser"),
            fullname=Username("User Userson"),
            email=Email("foo@bar.com"),
        )
        sqlalchemy_auth_user_repository.save(auth_user)
        auth_user.username = "someUser"

        with pytest.raises(IntegrityError):
            sqlalchemy_auth_user_repository.save(auth_user)

    def test_inserting_same_email_twice_should_fail(
        self, sqlalchemy_auth_user_repository
    ):
        auth_user = AuthUser(
            id=0,
            username=Username("someuser"),
            fullname=Username("User Userson"),
            email=Email("foo@bar.com"),
        )
        sqlalchemy_auth_user_repository.save(auth_user)
        auth_user.username = Username("someothername")

        with pytest.raises(IntegrityError):
            sqlalchemy_auth_user_repository.save(auth_user)

    def test_inserting_same_email_different_casing_twice_should_fail(
        self, sqlalchemy_auth_user_repository
    ):
        auth_user = AuthUser(
            id=0,
            username=Username("someuser"),
            fullname=Username("User Userson"),
            email=Email("foo@bar.com"),
        )
        sqlalchemy_auth_user_repository.save(auth_user)
        auth_user.username = Username("someothername")
        auth_user.email = Email("Foo@Bar.com")

        with pytest.raises(IntegrityError):
            sqlalchemy_auth_user_repository.save(auth_user)


class TestByUsername:
    def test_find_by_username_should_return_existing_user(
        self, sqlalchemy_auth_user_repository
    ):
        auth_user = AuthUser(
            id=0,
            username=Username("someuser"),
            fullname=Username("User Userson"),
            email=Email("foo@bar.com"),
        )
        auth_user = sqlalchemy_auth_user_repository.save(auth_user)

        found_user = sqlalchemy_auth_user_repository.find_by_username(
            Username("someuser")
        )

        assert found_user == auth_user

    def test_find_by_username_should_return_none_for_not_existing_user(
        self,
        sqlalchemy_auth_user_repository,
    ):
        found_user = sqlalchemy_auth_user_repository.find_by_username(
            Username("someuser")
        )

        assert found_user is None

    def test_exists_by_username_should_return_true(
        self, sqlalchemy_auth_user_repository
    ):
        auth_user = AuthUser(
            id=0,
            username=Username("someuser"),
            fullname=Username("User Userson"),
            email=Email("foo@bar.com"),
        )
        sqlalchemy_auth_user_repository.save(auth_user)

        assert sqlalchemy_auth_user_repository.exists_by_username(Username("someuser"))

    def test_exists_by_username_should_return_false(
        self,
        sqlalchemy_auth_user_repository,
    ):
        assert not sqlalchemy_auth_user_repository.find_by_username(
            Username("someuser")
        )


class TestByEmail:
    def test_find_by_email_should_return_existing_user(
        self, sqlalchemy_auth_user_repository
    ):
        auth_user = AuthUser(
            id=0,
            username=Username("someuser"),
            fullname=Username("User Userson"),
            email=Email("foo@bar.com"),
        )
        auth_user = sqlalchemy_auth_user_repository.save(auth_user)

        found_user = sqlalchemy_auth_user_repository.find_by_email(Email("foo@bar.com"))

        assert found_user == auth_user

    def test_find_by_email_should_return_none_for_not_existing_user(
        self,
        sqlalchemy_auth_user_repository,
    ):
        found_user = sqlalchemy_auth_user_repository.find_by_email(Email("foo@bar.com"))

        assert found_user is None

    def test_exists_by_email_should_return_true(self, sqlalchemy_auth_user_repository):
        auth_user = AuthUser(
            id=0,
            username=Username("someuser"),
            fullname=Username("User Userson"),
            email=Email("foo@bar.com"),
        )
        sqlalchemy_auth_user_repository.save(auth_user)

        assert sqlalchemy_auth_user_repository.exists_by_email(Email("foo@bar.com"))

    def test_exists_by_email_should_return_false(
        self,
        sqlalchemy_auth_user_repository,
    ):
        assert not sqlalchemy_auth_user_repository.exists_by_email(Email("foo@bar.com"))
