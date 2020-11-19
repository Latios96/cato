from dataclasses import dataclass, field
from typing import List, Iterable, Tuple, Dict

from cato.domain.test import Test
from cato.domain.test_identifier import TestIdentifier


@dataclass
class TestSuite:
    name: str
    tests: List[Test]
    variables: Dict[str, str] = field(default_factory=dict)

    def to_dict(self):
        return {"name": self.name, "tests": [x.to_dict() for x in self.tests]}


def iterate_suites_and_tests(
    suites: List[TestSuite],
) -> Iterable[Tuple[TestSuite, Test]]:
    for suite in suites:
        for test in suite.tests:
            yield suite, test


def count_suites(suites: List[TestSuite]) -> int:
    return len(suites)


def count_tests(suites: List[TestSuite]) -> int:
    return sum(map(lambda x: len(x.tests), suites))


def filter_by_suite_name(suites: List[TestSuite], name: str) -> List[TestSuite]:
    return list(filter(lambda x: x.name == name, suites))


def filter_by_test_identifier(
    suites: List[TestSuite], test_identifier: TestIdentifier
) -> List[TestSuite]:
    for suite, test in iterate_suites_and_tests(suites):
        if suite.name != test_identifier.suite_name:
            continue
        if test.name != test_identifier.test_name:
            continue
        return [TestSuite(name=suite.name, tests=[test])]
    return []
