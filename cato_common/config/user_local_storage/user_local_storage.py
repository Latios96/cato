from dataclasses import dataclass, field
from typing import Dict

from cato_common.domain.auth.api_token_str import ApiTokenStr


@dataclass
class UserLocalStorage:
    api_tokens: Dict[str, ApiTokenStr] = field(default_factory=dict)
