import logging
from dataclasses import dataclass

from cato_server.domain.auth.auth_user import AuthUser
from cato_common.domain.auth.email import Email
from cato_common.domain.auth.username import Username
from cato_server.storage.abstract.auth_user_repository import (
    AuthUserRepository,
)

logger = logging.getLogger(__name__)


@dataclass
class CreateUserData:
    username: Username
    fullname: Username
    email: Email


class UsernameAlreadyExistsException(Exception):
    def __init__(self):
        super(UsernameAlreadyExistsException, self).__init__(
            "User with this username already exists."
        )


class EmailAlreadyExistsException(Exception):
    def __init__(self):
        super(EmailAlreadyExistsException, self).__init__(
            "User with this email already exists."
        )


class CreateUser:
    def __init__(
        self,
        auth_user_repository: AuthUserRepository,
    ):
        self._auth_user_repository = auth_user_repository

    def create_user(self, create_user_data: CreateUserData) -> AuthUser:
        username_already_exists = self._auth_user_repository.exists_by_username(
            create_user_data.username
        )

        if username_already_exists:
            # Note: We consider this safe, because only already registered users should be allowed to create a new user
            raise UsernameAlreadyExistsException()

        email_already_exists = self._auth_user_repository.exists_by_email(
            create_user_data.email
        )
        if email_already_exists:
            # Note: We consider this safe, because only already registered users should be allowed to create a new user
            raise EmailAlreadyExistsException()

        auth_user = AuthUser(
            id=0,
            username=create_user_data.username,
            fullname=create_user_data.fullname,
            email=create_user_data.email,
        )
        auth_user = self._auth_user_repository.save(auth_user)

        logger.info('Created user "%s"', auth_user.username)

        return auth_user

    def create_or_update_user(self, create_user_data: CreateUserData):
        auth_user = self._auth_user_repository.find_by_username(
            create_user_data.username
        )
        if not auth_user:
            return self.create_user(create_user_data)

        auth_user.fullname = create_user_data.fullname
        auth_user.email = create_user_data.email

        auth_user = self._auth_user_repository.save(auth_user)

        logger.info('Updated user "%s"', auth_user.username)

        return auth_user
