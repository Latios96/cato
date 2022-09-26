from dataclasses import dataclass
from typing import List, Optional, Dict

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.branch_name import BranchName
from cato_common.domain.run_batch_identifier import RunBatchIdentifier
from cato_common.domain.run_batch_provider import RunBatchProvider
from cato_common.domain.run_information import OS
from cato_common.domain.test_identifier import TestIdentifier


@dataclass
class TestForRunCreation:
    test_name: str
    test_identifier: TestIdentifier
    test_command: str
    test_variables: Dict[str, str]
    comparison_settings: ComparisonSettings


@dataclass
class TestSuiteForRunCreation:
    suite_name: str
    suite_variables: Dict[str, str]
    tests: List[TestForRunCreation]


@dataclass
class BasicRunInformationForRunCreation:
    os: OS
    computer_name: str
    __json_type_info_attribute__ = "run_information_type"

    def __post_init__(self):
        self.run_information_type = None


@dataclass
class LocalComputerRunInformationForRunCreation(BasicRunInformationForRunCreation):
    local_username: str
    run_information_type = RunBatchProvider.LOCAL_COMPUTER

    @staticmethod
    def from_basic_run(basic_run, local_username):
        # type: (BasicRunInformationForRunCreation,str)->LocalComputerRunInformationForRunCreation
        return LocalComputerRunInformationForRunCreation(
            os=basic_run.os,
            computer_name=basic_run.computer_name,
            local_username=local_username,
        )

    def __post_init__(self):
        self.run_information_type = RunBatchProvider.LOCAL_COMPUTER


@dataclass
class GithubActionsRunInformationForRunCreation(BasicRunInformationForRunCreation):
    github_run_id: int
    html_url: str
    job_name: str
    actor: str
    attempt: int
    run_number: int
    github_url: str
    github_api_url: str
    run_information_type = RunBatchProvider.GITHUB_ACTIONS

    @staticmethod
    def from_basic_run(
        basic_run,
        github_run_id,
        html_url,
        job_name,
        actor,
        attempt,
        run_number,
        github_url,
        github_api_url,
    ):
        # type: (BasicRunInformationForRunCreation,int,str,str,str,int,int,str,str)->GithubActionsRunInformationForRunCreation
        return GithubActionsRunInformationForRunCreation(
            os=basic_run.os,
            computer_name=basic_run.computer_name,
            github_run_id=github_run_id,
            html_url=html_url,
            job_name=job_name,
            actor=actor,
            attempt=attempt,
            run_number=run_number,
            github_url=github_url,
            github_api_url=github_api_url,
        )

    def __post_init__(self):
        self.run_information_type = RunBatchProvider.GITHUB_ACTIONS


@dataclass
class CreateFullRunDto:
    project_id: int
    run_batch_identifier: RunBatchIdentifier
    test_suites: List[TestSuiteForRunCreation]
    run_information: BasicRunInformationForRunCreation
    branch_name: Optional[BranchName] = None
