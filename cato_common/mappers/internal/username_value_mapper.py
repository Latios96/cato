from typing import Optional

from cato_common.domain.auth.username import Username
from cato_common.mappers.abstract_value_mapper import AbstractValueMapper


class UsernameValueMapper(AbstractValueMapper[Username, str]):
    def map_from(self, username_str: Optional[str]) -> Optional[Username]:
        if not username_str:
            return None
        return Username(username_str)

    def map_to(self, username: Username) -> str:
        return str(username)
