from typing import TypeVar, Type, Union, Callable
from unittest import mock

T = TypeVar("T")


def mock_safe(cls: Type[T]) -> T:
    return mock.MagicMock()


def or_default(value: T, default_value: Union[T, Callable[[], T]]):
    if value is "FORCE_NONE":
        return None

    if value is not None:
        return value

    if callable(default_value):
        return default_value()
    return default_value
