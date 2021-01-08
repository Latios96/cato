from enum import Enum


class VerboseMode(Enum):
    DEFAULT = 1
    VERBOSE = 2
    VERY_VERBOSE = 3

    def includes(self, value):
        return self.value >= value.value
