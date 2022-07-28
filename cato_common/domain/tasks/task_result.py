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
    result_: Optional[T]
    error_message_: Optional[str]

    @property
    def result(self) -> T:
        if not self.state == TaskResultState.SUCCESS or self.result_ is None:
            raise IllegalStateError(
                f"Can't get a result of a TaskResult with state {self.state}"
            )
        return self.result_

    @property
    def error_message(self):
        if not self.state == TaskResultState.FAILURE:
            raise IllegalStateError(
                f"Can't get n error message of a TaskResult with state {self.state}"
            )
        return self.error_message_
