from dataclasses import dataclass
from typing import List, Optional, Dict

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.branch_name import BranchName
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
class CreateFullRunDto:
    project_id: int
    test_suites: List[TestSuiteForRunCreation]
    branch_name: Optional[BranchName] = None
