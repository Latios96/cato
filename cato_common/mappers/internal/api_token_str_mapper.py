from typing import Optional

from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_common.mappers.abstract_value_mapper import AbstractValueMapper


class ApiTokenStrValueMapper(AbstractValueMapper[ApiTokenStr, str]):
    def map_from(self, api_token_str: Optional[str]) -> Optional[ApiTokenStr]:
        if not api_token_str:
            return None
        return ApiTokenStr(api_token_str)

    def map_to(self, api_token_str: ApiTokenStr) -> str:
        return str(api_token_str)
