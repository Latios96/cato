from dataclasses import dataclass
from typing import List, Iterable, Tuple

from cato.domain.test import Test


@dataclass
class TestSuite:
    name: str
    tests: List[Test]

    def to_dict(self):
        return {"name": self.name, "tests": [x.to_dict() for x in self.tests]}


def iterate_suites_and_tests(
    suites: List[TestSuite],
) -> Iterable[Tuple[TestSuite, Test]]:
    for suite in suites:
        for test in suite.tests:
            yield suite, test

