import datetime
from dataclasses import dataclass

from cato_common.domain.auth.api_token_id import ApiTokenId
from cato_common.domain.auth.api_token_name import ApiTokenName


@dataclass
class ApiToken:
    name: ApiTokenName
    id: ApiTokenId
    created_at: datetime.datetime
    expires_at: datetime.datetime
