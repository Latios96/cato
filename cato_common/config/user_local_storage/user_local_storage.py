from dataclasses import dataclass, field
from typing import Dict, Optional

from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_common.domain.machine_info import MachineInfo


@dataclass
class UserLocalStorage:
    machine_info: Optional[MachineInfo] = field(default=None)
    api_tokens: Dict[str, ApiTokenStr] = field(default_factory=dict)
