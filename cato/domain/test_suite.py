from dataclasses import dataclass
from typing import List

from cato.domain.test import Test


@dataclass
class TestSuite:
    name: str
    tests: List[Test]
