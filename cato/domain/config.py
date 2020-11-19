from dataclasses import dataclass, field
from typing import List, Dict

from cato.domain.test_suite import TestSuite


@dataclass
class Config:
    path: str
    test_suites: List[TestSuite]
    output_folder: str
    variables: Dict[str, str] = field(default_factory=dict)

    def for_json(self):
        return {"suites": self.test_suites, "variables": self.variables}
