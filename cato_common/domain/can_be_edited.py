from dataclasses import dataclass
from typing import Optional


@dataclass
class CanBeEdited:
    can_edit: bool
    message: Optional[str]

    @staticmethod
    def yes():
        # type: ()->CanBeEdited
        return CanBeEdited(True, None)

    @staticmethod
    def no(message):
        # type: (str)->CanBeEdited
        return CanBeEdited(False, message)
