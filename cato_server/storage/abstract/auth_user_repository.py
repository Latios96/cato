from typing import Optional

from cato_server.domain.auth.auth_user import AuthUser
from cato_common.domain.auth.email import Email
from cato_common.domain.auth.username import Username
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class AuthUserRepository(AbstractRepository[AuthUser, int]):
    def find_by_username(self, username: Username) -> Optional[AuthUser]:
        raise NotImplementedError()

    def find_by_email(self, email: Email) -> Optional[AuthUser]:
        raise NotImplementedError()

    def exists_by_username(self, username: Username) -> bool:
        raise NotImplementedError()

    def exists_by_email(self, email: Email) -> bool:
        raise NotImplementedError()
