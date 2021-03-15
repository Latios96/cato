from dataclasses import dataclass, field
from typing import List, Dict

from cato.domain.test_suite import TestSuite


@dataclass
class Config:
    project_name: str
    path: str
    test_suites: List[TestSuite]
    output_folder: str
    variables: Dict[str, str] = field(default_factory=dict)

    def for_json(self):
        return {
            "project_name": self.project_name,
            "suites": self.test_suites,
            "variables": self.variables,
        }

    @property
    def suite_count(self):
        return len(self.test_suites)

    @property
    def test_count(self):
        return sum(map(lambda x: len(x.tests), self.test_suites))
