from dataclasses import dataclass
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


@dataclass
class OptionalComponent(Generic[T]):
    component: Optional[T]

    @staticmethod
    def empty():
        return OptionalComponent(None)

    def is_available(self) -> bool:
        return self.component is not None
