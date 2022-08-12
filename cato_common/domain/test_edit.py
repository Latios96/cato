import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import TypeVar, Optional

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.test_identifier import TestIdentifier

T = TypeVar("T")


class EditTypes(Enum):
    COMPARISON_SETTINGS = "COMPARISON_SETTINGS"
    REFERENCE_IMAGE = "REFERENCE_IMAGE"


@dataclass
class AbstractTestEdit:
    id: int
    test_id: int
    test_identifier: TestIdentifier
    created_at: datetime.datetime

    def __post_init__(self):
        self.edit_type = None


@dataclass
class ComparisonSettingsEditValue:
    comparison_settings: ComparisonSettings
    status: ResultStatus
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
    reference_image_id: int
    diff_image_id: int
    error_value: float
    status: ResultStatus
    message: Optional[str]


@dataclass
class ReferenceImageEdit(AbstractTestEdit):
    new_value: ReferenceImageEditValue
    old_value: ReferenceImageEditValue
    edit_type: EditTypes = field(default_factory=lambda: EditTypes.REFERENCE_IMAGE)

    def __post_init__(self):
        self.edit_type = EditTypes.REFERENCE_IMAGE
