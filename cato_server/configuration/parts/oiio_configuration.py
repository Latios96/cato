from dataclasses import dataclass
from typing import Optional


@dataclass
class OiioConfiguration:
    thread_count: Optional[int]
