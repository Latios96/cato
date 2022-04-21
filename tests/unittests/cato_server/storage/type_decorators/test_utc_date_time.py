import datetime

import pytest

from cato_server.storage.sqlalchemy.type_decorators.utc_date_time import UtcDateTime


@pytest.mark.parametrize(
    "value,expected_result",
    [
        (None, None),
        (
            datetime.datetime(2022, 4, 21, 16, 0, tzinfo=datetime.timezone.utc),
            datetime.datetime(2022, 4, 21, 16, 0),
        ),
        (
            datetime.datetime(
                2022,
                4,
                21,
                16,
                0,
                tzinfo=datetime.timezone(datetime.timedelta(hours=1)),
            ),
            datetime.datetime(2022, 4, 21, 15, 0),
        ),
    ],
)
def test_process_bind_param(value, expected_result):
    result = UtcDateTime().process_bind_param(value, "postgres")

    assert result == expected_result


def test_process_bind_param_fail_for_non_datetime_value():
    with pytest.raises(TypeError):
        UtcDateTime().process_bind_param("value", "postgres")


def test_process_bind_param_fail_for_naive_datetime_object():
    with pytest.raises(ValueError):
        UtcDateTime().process_bind_param(
            datetime.datetime(2022, 4, 21, 16, 0), "postgres"
        )


@pytest.mark.parametrize(
    "value,expected_result",
    [
        (None, None),
        (
            datetime.datetime(2022, 4, 21, 16, 0),
            datetime.datetime(2022, 4, 21, 16, 0, tzinfo=datetime.timezone.utc),
        ),
    ],
)
def test_process_result_value(value, expected_result):
    result = UtcDateTime().process_result_value(value, "postgres")

    assert result == expected_result


def test_process_bind_param_fail_for_not_naive_datetime_object():
    with pytest.raises(ValueError):
        UtcDateTime().process_result_value(
            datetime.datetime(2022, 4, 21, 16, 0, tzinfo=datetime.timezone.utc),
            "postgres",
        )
