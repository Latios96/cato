import pytest

from cato.domain.comparison_settings import ComparisonSettings
from cato.domain.test import Test
from cato_common.domain.test_identifier import TestIdentifier
from cato.domain.test_suite import (
    TestSuite,
    iterate_suites_and_tests,
    count_suites,
    count_tests,
    filter_by_suite_name,
    filter_by_test_identifier,
    filter_by_test_identifiers,
    find_test_by_test_identifier,
)

test1 = Test("test1", "command", {}, ComparisonSettings.default())
test2 = Test("test2", "command", {}, ComparisonSettings.default())
test3 = Test("test3", "command", {}, ComparisonSettings.default())
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


def test_find_test_by_test_identifier_should_find():
    filter_result = find_test_by_test_identifier(
        suites, TestIdentifier.from_string("my_suite_2/test2")
    )

    assert filter_result == test2


def test_find_test_by_test_identifier_should_not_find():
    filter_result = find_test_by_test_identifier(
        suites, TestIdentifier.from_string("my_suite_2/wurst")
    )

    assert filter_result == None


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
