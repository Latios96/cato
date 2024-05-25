from dataclasses import dataclass, field
from typing import Dict, Optional

from cato.domain.machine_info_cache_entry import MachineInfoCacheEntry
from cato_common.domain.auth.api_token_str import ApiTokenStr


@dataclass
class UserLocalStorage:
    machine_info_cache_entry: Optional[MachineInfoCacheEntry] = field(default=None)
    api_tokens: Dict[str, ApiTokenStr] = field(default_factory=dict)
