from typing import TypeVar, Type, Any, Optional

T = TypeVar("T")


def safe_cast(type_to_cast_to: Type[T], value: Any) -> T:
    if not isinstance(value, type_to_cast_to):
        raise RuntimeError(
            "Can not cast {} to {}".format(value.__claas__, type_to_cast_to)
        )
    return value


def safe_unwrap(optional: Optional[T]) -> T:
    if optional is None:
        raise ValueError("Tried to unwrap an optional, but it was None.")
    return optional
