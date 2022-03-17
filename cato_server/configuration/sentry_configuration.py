from dataclasses import dataclass
from typing import Optional


@dataclass
class SentryConfiguration:
    url: Optional[str]

    @staticmethod
    def default():
        return SentryConfiguration(url=None)
