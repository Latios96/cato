import sys
from dataclasses import dataclass
from enum import Enum

from cato_common.domain.run_batch_provider import RunBatchProvider


class OS(Enum):
    WINDOWS = "WINDOWS"
    LINUX = "LINUX"
    MAC_OS = "MAC_OS"
    UNKNOWN = "UNKNOWN"

    @staticmethod
    def get_current_os():
        # type: ()-> OS
        return {
            "win32": OS.WINDOWS,
            "linux": OS.LINUX,
            "darwin": OS.MAC_OS,
        }[sys.platform]


@dataclass
class BasicRunInformation:
    id: int
    run_id: int
    os: OS
    computer_name: str
    __json_type_info_attribute__ = "run_information_type"

    def __post_init__(self):
        self.run_information_type = None


@dataclass
class LocalComputerRunInformation(BasicRunInformation):
    local_username: str
    run_information_type = RunBatchProvider.LOCAL_COMPUTER

    def __post_init__(self):
        self.run_information_type = RunBatchProvider.LOCAL_COMPUTER


@dataclass
class GithubActionsRunInformation(BasicRunInformation):
    github_run_id: int
    job_id: int
    job_name: str
    actor: str
    attempt: int
    run_number: int
    github_url: str
    github_api_url: str
    run_information_type = RunBatchProvider.GITHUB_ACTIONS

    def __post_init__(self):
        self.run_information_type = RunBatchProvider.GITHUB_ACTIONS
