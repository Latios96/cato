from enum import Enum


class RunBatchProvider(str, Enum):
    LOCAL_COMPUTER = "LOCAL_COMPUTER"
    GITHUB_ACTIONS = "GITHUB_ACTIONS"
