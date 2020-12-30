import datetime

from cato_server.mappers.internal.datetime_value_mapper import DateTimeValueMapper


def test_map_from():
    date = datetime.datetime.now()
    wrapper = DateTimeValueMapper()

    result = wrapper.map_from(date.isoformat())

    assert result == date


def test_map_from_empty():
    wrapper = DateTimeValueMapper()

    result = wrapper.map_from(None)

    assert result is None


def test_map_to():
    date = datetime.datetime.now()
    wrapper = DateTimeValueMapper()

    result = wrapper.map_to(date)

    assert result == date.isoformat()
