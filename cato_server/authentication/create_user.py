from dataclasses import dataclass

from cato_server.authentication.crypto_context import CryptoContext
from cato_server.domain.auth.auth_user import AuthUser
from cato_server.domain.auth.secret_str import SecretStr
from cato_server.domain.auth.username import Username
from cato_server.storage.abstract.abstract_auth_user_repository import (
    AbstractAuthUserRepository,
)

import logging

logger = logging.getLogger(__name__)


@dataclass
class CreateUserData:
    username: Username
    password: SecretStr


class UsernameAlreadyExistsException(Exception):
    def __init__(self):
        super(UsernameAlreadyExistsException, self).__init__(
            "User with this username already exists."
        )


class CreateUser:
    def __init__(
        self,
        auth_user_repository: AbstractAuthUserRepository,
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

        hashed_password = self._crypto_context.hash_password(
            create_user_data.password.get_secret_value()
        )

        auth_user = AuthUser(
            id=0,
            username=create_user_data.username,
            hashed_password=SecretStr(hashed_password),
        )
        auth_user = self._auth_user_repository.save(auth_user)

        logger.info('Created user with name "%s"', auth_user.username)

        return auth_user
