from dataclasses import dataclass

from typing import List

import pytest


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
