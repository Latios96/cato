from __future__ import annotations
from enum import Enum


class VerboseMode(Enum):
    DEFAULT = 1
    VERBOSE = 2
    VERY_VERBOSE = 3

    @staticmethod
    def in_range(value: int) -> VerboseMode:
        if value < 1:
            value = 1
        if value > 3:
            value = 3
        return VerboseMode(value)

    def includes(self, value):
        return self.value >= value.value
