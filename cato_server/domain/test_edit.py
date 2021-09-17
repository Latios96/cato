import datetime
from dataclasses import dataclass
from enum import Enum
from typing import TypeVar, Dict

from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings

T = TypeVar("T")


class EditTypes(Enum):
    COMPARISON_SETTINGS = "COMPARISON_SETTINGS"
    REFERENCE_IMAGE = "REFERENCE_IMAGE"


@dataclass
class TestEdit:
    id: int
    test_id: int
    edit_type: EditTypes
    created_at: datetime.datetime
    old_value: Dict
    new_value: Dict


@dataclass
class ComparisonSettingsEdit:
    id: int
    test_id: int
    edit_type = EditTypes.COMPARISON_SETTINGS
    created_at: datetime.datetime
    old_value: ComparisonSettings
    new_value: ComparisonSettings

    @staticmethod
    def from_test_edit(test_edit: TestEdit):
        if not test_edit.edit_type == EditTypes.COMPARISON_SETTINGS:
            raise ValueError(f"Invalid edit type: {test_edit.edit_type}")
        return ComparisonSettingsEdit(
            id=test_edit.id,
            test_id=test_edit.test_id,
            created_at=test_edit.created_at,
            old_value=ComparisonSettings(
                method=ComparisonMethod(test_edit.old_value["method"]),
                threshold=test_edit.old_value["threshold"],
            ),
            new_value=ComparisonSettings(
                method=ComparisonMethod(test_edit.new_value["method"]),
                threshold=test_edit.new_value["threshold"],
            ),
        )

    def to_test_edit(self):
        return TestEdit(
            id=self.id,
            test_id=self.test_id,
            edit_type=EditTypes.COMPARISON_SETTINGS,
            created_at=self.created_at,
            old_value={
                "method": self.old_value.method.value,
                "threshold": self.old_value.threshold,
            },
            new_value={
                "method": self.new_value.method.value,
                "threshold": self.new_value.threshold,
            },
        )
