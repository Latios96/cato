import pytest

from cato.domain.test import Test
from cato_server.domain.test_identifier import TestIdentifier
from cato.domain.test_suite import (
    TestSuite,
    iterate_suites_and_tests,
    count_suites,
    count_tests,
    filter_by_suite_name,
    filter_by_test_identifier,
    filter_by_test_identifiers,
)

test1 = Test("test1", "command", {})
test2 = Test("test2", "command", {})
test3 = Test("test3", "command", {})
suite1 = TestSuite(name="my_suite_1", tests=[test1])
suite2 = TestSuite(name="my_suite_2", tests=[test2, test3])

suites = [suite1, suite2]


def test_iterate_suites_and_tests():
    iterate_result = list(iterate_suites_and_tests(suites))

    assert iterate_result == [
        (suite1, test1),
        (suite2, test2),
        (suite2, test3),
    ]


def test_count_suites():
    assert count_suites(suites) == 2


def test_count_tests():
    assert count_tests(suites) == 3


def test_filter_by_suite_name():
    filter_result = filter_by_suite_name(suites, "my_suite_1")

    assert filter_result == [suite1]


def test_filter_by_test_identifier():
    filter_result = filter_by_test_identifier(
        suites, TestIdentifier.from_string("my_suite_2/test2")
    )

    assert filter_result == [TestSuite(name="my_suite_2", tests=[test2])]


@pytest.mark.parametrize(
    "identifiers,expected",
    [
        (
            [TestIdentifier.from_string("my_suite_2/test2")],
            [TestSuite(name="my_suite_2", tests=[test2])],
        ),
        (
            [
                TestIdentifier.from_string("my_suite_2/test2"),
                TestIdentifier.from_string("my_suite/test1"),
            ],
            [TestSuite(name="my_suite_2", tests=[test2])],
        ),
        (
            [
                TestIdentifier.from_string("my_suite_2/test2"),
                TestIdentifier.from_string("my_suite_1/test1"),
            ],
            [
                TestSuite(name="my_suite_1", tests=[test1]),
                TestSuite(name="my_suite_2", tests=[test2]),
            ],
        ),
    ],
)
def test_filter_by_test_identifiers(identifiers, expected):
    filter_result = filter_by_test_identifiers(suites, identifiers)

    assert filter_result == expected