from dataclasses import dataclass, field
from typing import List, Iterable, Tuple, Dict, Optional

from cato.domain.test import Test
from cato.domain.validation import validate_name
from cato_common.domain.test_identifier import TestIdentifier


@dataclass
class TestSuite:
    name: str
    tests: List[Test]
    variables: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        validate_name(self.name)

    __test__ = False


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
        return [TestSuite(name=suite.name, tests=[test], variables=suite.variables)]
    return []


def find_test_by_test_identifier(
    suites: List[TestSuite], test_identifier: TestIdentifier
) -> Optional[Test]:
    for suite, test in iterate_suites_and_tests(suites):
        if suite.name != test_identifier.suite_name:
            continue
        if test.name != test_identifier.test_name:
            continue
        return test
    return None


def filter_by_test_identifiers(
    suites: List[TestSuite], test_identifiers: List[TestIdentifier]
) -> List[TestSuite]:
    suites_by_name: Dict[str, TestSuite] = {}
    for suite, test in iterate_suites_and_tests(suites):
        for test_identifier in test_identifiers:
            if suite.name != test_identifier.suite_name:
                continue
            if test.name != test_identifier.test_name:
                continue
            filtered_suite = suites_by_name.get(suite.name)
            if not filtered_suite:
                filtered_suite = TestSuite(
                    name=suite.name, tests=[], variables=suite.variables
                )
                suites_by_name[suite.name] = filtered_suite
            filtered_suite.tests.append(test)
    return list(suites_by_name.values())
