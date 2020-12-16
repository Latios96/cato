from attr import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")


@dataclass
class Event(Generic[T]):
    event_name: str
    value: T
