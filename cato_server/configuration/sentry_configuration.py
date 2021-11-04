from dataclasses import dataclass
from typing import Optional


@dataclass
class SentryConfiguration:
    url: Optional[str]
