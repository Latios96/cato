from typing import Optional

from cato_server.domain.auth_user import AuthUser
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class AbstractAuthUserRepository(AbstractRepository[AuthUser, int]):
    def find_by_username(self, username_str) -> Optional[AuthUser]:
        raise NotImplementedError()
