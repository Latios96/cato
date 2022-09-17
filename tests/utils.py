from typing import TypeVar, Type, Union, Callable
from unittest import mock

T = TypeVar("T")


def mock_safe(cls: Type[T]) -> T:
    return mock.MagicMock()


def or_default(value, default_value):
    if value is "FORCE_NONE":
        return None
    if value is None:
        return default_value
    return value
