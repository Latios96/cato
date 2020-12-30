import pytest

from cato.domain.test_status import TestStatus
from cato_server.mappers.internal.test_status_value_mapper import TestStatusValueMapper


@pytest.mark.parametrize(
    "value,expected",
    [
        ("SUCCESS", TestStatus.SUCCESS),
        ("FAILED", TestStatus.FAILED),
    ],
)
def test_map_from(value, expected):
    wrapper = TestStatusValueMapper()

    result = wrapper.map_from(value)

    assert result == expected


def test_map_from_empty():
    wrapper = TestStatusValueMapper()

    result = wrapper.map_from(None)

    assert result is None


@pytest.mark.parametrize(
    "value,expected",
    [
        (TestStatus.SUCCESS, "SUCCESS"),
        (TestStatus.FAILED, "FAILED"),
    ],
)
def test_map_to(value, expected):
    wrapper = TestStatusValueMapper()

    result = wrapper.map_to(value)

    assert result == expected
