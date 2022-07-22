from dataclasses import dataclass
from enum import Enum
from typing import Generic, TypeVar, Optional

T = TypeVar("T")


class TaskResultState(Enum):
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"


class IllegalStateError(RuntimeError):
    pass


@dataclass(frozen=True)
class TaskResult(Generic[T]):
    task_id: str
    state: TaskResultState
    url: str
    _result: Optional[T]
    _error_message: Optional[str]

    @property
    def result(self) -> T:
        if not self.state == TaskResultState.SUCCESS:
            raise IllegalStateError(
                f"Can't get a result of a TaskResult with state {self.state}"
            )
        return self._result

    @property
    def error_message(self):
        if not self.state == TaskResultState.FAILURE:
            raise IllegalStateError(
                f"Can't get n error message of a TaskResult with state {self.state}"
            )
        return self._error_message
