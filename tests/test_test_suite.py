from cato.domain.test import Test
from cato.domain.test_suite import (
    TestSuite,
    iterate_suites_and_tests,
    count_suites,
    count_tests,
    filter_by_suite_name,
)

test1 = Test("test1", "command", {})
test2 = Test("test1", "command", {})
test3 = Test("test1", "command", {})
suite1 = TestSuite(name="my suite 1", tests=[test1])
suite2 = TestSuite(name="my suite 2", tests=[test2, test3])

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
    filter_result = filter_by_suite_name(suites, "my suite 1")

    assert filter_result == [suite1]
