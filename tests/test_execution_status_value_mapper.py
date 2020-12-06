import pytest

from cato.mappers.execution_status_value_mapper import ExecutionStatusValueMapper
from cato_server.storage.domain.execution_status import ExecutionStatus


@pytest.mark.parametrize(
    "value,expected",
    [
        ("NOT_STARTED", ExecutionStatus.NOT_STARTED),
        ("RUNNING", ExecutionStatus.RUNNING),
        ("FINISHED", ExecutionStatus.FINISHED),
    ],
)
def test_map_from(value, expected):
    wrapper = ExecutionStatusValueMapper()

    result = wrapper.map_from(value)

    assert result == expected


def test_map_from_empty():
    wrapper = ExecutionStatusValueMapper()

    result = wrapper.map_from(None)

    assert result is None


@pytest.mark.parametrize(
    "value,expected",
    [
        (ExecutionStatus.NOT_STARTED, "NOT_STARTED"),
        (ExecutionStatus.RUNNING, "RUNNING"),
        (ExecutionStatus.FINISHED, "FINISHED"),
    ],
)
def test_map_to(value, expected):
    wrapper = ExecutionStatusValueMapper()

    result = wrapper.map_to(value)

    assert result == expected
