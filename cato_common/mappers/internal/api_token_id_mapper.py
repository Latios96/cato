from typing import Optional

from cato_common.domain.auth.api_token_id import ApiTokenId
from cato_common.mappers.abstract_value_mapper import AbstractValueMapper


class ApiTokenIdValueMapper(AbstractValueMapper[ApiTokenId, str]):
    def map_from(self, api_token_id: Optional[str]) -> Optional[ApiTokenId]:
        if not api_token_id:
            return None
        return ApiTokenId(api_token_id)

    def map_to(self, api_token_id: ApiTokenId) -> str:
        return str(api_token_id)
