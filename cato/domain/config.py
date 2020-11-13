from dataclasses import dataclass
from typing import List

from cato.domain.test_suite import TestSuite


@dataclass
class Config:
    path: str
    test_suites: List[TestSuite]
