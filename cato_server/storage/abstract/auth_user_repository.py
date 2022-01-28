from typing import Optional

from cato_server.domain.auth.auth_user import AuthUser
from cato_server.domain.auth.username import Username
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class AuthUserRepository(AbstractRepository[AuthUser, int]):
    def find_by_username(self, username: Username) -> Optional[AuthUser]:
        raise NotImplementedError()
