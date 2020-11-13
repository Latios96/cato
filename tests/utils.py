from typing import TypeVar, Type
from unittest import mock

T = TypeVar("T")


def mock_safe(cls: Type[T]) -> T:
    return mock.MagicMock()
