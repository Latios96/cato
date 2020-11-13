from dataclasses import dataclass
from typing import List

from cato.domain.Test import Test


@dataclass
class TestSuite:
    name: str
    tests: List[Test]
