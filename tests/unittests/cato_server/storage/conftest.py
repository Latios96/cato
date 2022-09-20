from contextlib import contextmanager
from dataclasses import dataclass

from typing import List

import pytest
import sqltap


@dataclass
class OrderingTestData:
    wrong_order: List[str]
    correct_order_lowercase: List[str]


@pytest.fixture
def order_test_data():
    return OrderingTestData(
        wrong_order=["zzz", "c", "B", "A", "M", "a"],
        correct_order_lowercase=["a", "a", "b", "c", "m", "zzz"],
    )


class QueryCountNotMatching(Exception):
    def __init__(self, expected, actual):
        super(QueryCountNotMatching, self).__init__(
            f"Query count not matching, expected {expected} queries, was {actual}"
        )


@contextmanager
def sqltap_asserter(expected_query_count: int):
    profiler = sqltap.start()
    yield
    statistics = profiler.collect()
    profiler.stop()

    expected_query_count_not_matching = expected_query_count != len(statistics)

    if expected_query_count_not_matching:
        print("\n\n")
        print("Queries run:")
        for query in statistics:
            print("")
            print(query.text)
        raise QueryCountNotMatching(expected_query_count, len(statistics))
