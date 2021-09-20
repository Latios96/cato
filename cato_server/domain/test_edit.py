import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import TypeVar, Optional

from cato.domain.comparison_settings import ComparisonSettings
from cato.domain.test_status import TestStatus

T = TypeVar("T")


class EditTypes(Enum):
    COMPARISON_SETTINGS = "COMPARISON_SETTINGS"
    REFERENCE_IMAGE = "REFERENCE_IMAGE"


@dataclass
class AbstractTestEdit:
    id: int
    test_id: int
    created_at: datetime.datetime

    def __post_init__(self):
        self.edit_type = None


@dataclass
class ComparisonSettingsEditValue:
    comparison_settings: ComparisonSettings
    status: TestStatus
    message: Optional[str]
    diff_image_id: int
    error_value: float


@dataclass
class ComparisonSettingsEdit(AbstractTestEdit):
    new_value: ComparisonSettingsEditValue
    old_value: ComparisonSettingsEditValue
    edit_type: EditTypes = field(default_factory=lambda: EditTypes.COMPARISON_SETTINGS)

    def __post_init__(self):
        self.edit_type = EditTypes.COMPARISON_SETTINGS


@dataclass
class ReferenceImageEditValue:
    pass


@dataclass
class ReferenceImageEdit(AbstractTestEdit):
    edit_type: EditTypes = field(default_factory=lambda: EditTypes.REFERENCE_IMAGE)

    def __post_init__(self):
        self.edit_type = EditTypes.REFERENCE_IMAGE
