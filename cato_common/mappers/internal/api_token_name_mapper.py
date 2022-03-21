from typing import Optional

from cato_common.domain.auth.api_token_name import ApiTokenName
from cato_common.mappers.abstract_value_mapper import AbstractValueMapper


class ApiTokenNameValueMapper(AbstractValueMapper[ApiTokenName, str]):
    def map_from(self, api_token_name: Optional[str]) -> Optional[ApiTokenName]:
        if not api_token_name:
            return None
        return ApiTokenName(api_token_name)

    def map_to(self, api_token_name: ApiTokenName) -> str:
        return str(api_token_name)
