import logging
from dataclasses import dataclass

from cato_server.authentication.crypto_context import CryptoContext
from cato_server.domain.auth.auth_user import AuthUser
from cato_server.domain.auth.email import Email
from cato_server.domain.auth.username import Username
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
        crypto_context: CryptoContext,
    ):
        self._auth_user_repository = auth_user_repository
        self._crypto_context = crypto_context

    def create_user(self, create_user_data: CreateUserData) -> AuthUser:
        username_already_exists = (
            self._auth_user_repository.find_by_username(create_user_data.username)
            is not None
        )
        if username_already_exists:
            # Note: We consider this safe, because only already registered users should be allowed to create a new user
            raise UsernameAlreadyExistsException()

        email_already_exists = (
            self._auth_user_repository.find_by_email(create_user_data.email) is not None
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
