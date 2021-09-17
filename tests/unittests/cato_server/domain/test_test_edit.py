import datetime

import pytest

from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings
from cato_server.domain.test_edit import TestEdit, EditTypes, ComparisonSettingsEdit

NOW = datetime.datetime.now()


class TestComparisonSettingsEdit:
    def test_from_test_edit(self):
        test_edit = TestEdit(
            id=0,
            test_id=1,
            edit_type=EditTypes.COMPARISON_SETTINGS,
            created_at=NOW,
            old_value={
                "method": "SSIM",
                "threshold": 1,
            },
            new_value={
                "method": "SSIM",
                "threshold": 10,
            },
        )

        comparison_settings_edit = ComparisonSettingsEdit.from_test_edit(test_edit)

        assert comparison_settings_edit == ComparisonSettingsEdit(
            id=0,
            test_id=1,
            created_at=NOW,
            old_value=ComparisonSettings(
                method=ComparisonMethod.SSIM,
                threshold=1,
            ),
            new_value=ComparisonSettings(
                method=ComparisonMethod.SSIM,
                threshold=10,
            ),
        )

    @pytest.mark.parametrize(
        "data,expected_exception",
        [
            (
                TestEdit(
                    id=0,
                    test_id=1,
                    edit_type=EditTypes.COMPARISON_SETTINGS,
                    created_at=NOW,
                    old_value={
                        "methdod": "SSIM",
                        "threshold": 1,
                    },
                    new_value={
                        "method": "SSIM",
                        "threshold": 10,
                    },
                ),
                KeyError,
            ),
            (
                TestEdit(
                    id=0,
                    test_id=1,
                    edit_type=EditTypes.COMPARISON_SETTINGS,
                    created_at=NOW,
                    old_value={
                        "method": "SSIM",
                        "threshold": 1,
                    },
                    new_value={
                        "method": "SSIM",
                        "threscold": 10,
                    },
                ),
                KeyError,
            ),
            (
                TestEdit(
                    id=0,
                    test_id=1,
                    edit_type=EditTypes.COMPARISON_SETTINGS,
                    created_at=NOW,
                    old_value={
                        "methdod": "SSIsM",
                        "threshold": 1,
                    },
                    new_value={
                        "method": "SSIM",
                        "threshold": 10,
                    },
                ),
                KeyError,
            ),
            (
                TestEdit(
                    id=0,
                    test_id=1,
                    edit_type=EditTypes.COMPARISON_SETTINGS,
                    created_at=NOW,
                    old_value={
                        "methdod": "SSIM",
                        "threshold": 1,
                    },
                    new_value={
                        "method": "SSsIM",
                        "threshold": 10,
                    },
                ),
                KeyError,
            ),
            (
                TestEdit(
                    id=0,
                    test_id=1,
                    edit_type=EditTypes.REFERENCE_IMAGE,
                    created_at=NOW,
                    old_value={
                        "method": "SSIM",
                        "threshold": 1,
                    },
                    new_value={
                        "method": "SSIM",
                        "threshold": 10,
                    },
                ),
                ValueError,
            ),
        ],
    )
    def test_from_test_edit_invalid_old_value(self, data, expected_exception):
        with pytest.raises(expected_exception):
            ComparisonSettingsEdit.from_test_edit(data)

    def test_to_test_edit(self):
        comparison_settings_edit = ComparisonSettingsEdit(
            id=0,
            test_id=1,
            created_at=NOW,
            old_value=ComparisonSettings(
                method=ComparisonMethod.SSIM,
                threshold=1,
            ),
            new_value=ComparisonSettings(
                method=ComparisonMethod.SSIM,
                threshold=10,
            ),
        )

        test_edit = comparison_settings_edit.to_test_edit()

        assert test_edit == TestEdit(
            id=0,
            test_id=1,
            edit_type=EditTypes.COMPARISON_SETTINGS,
            created_at=NOW,
            old_value={
                "method": "SSIM",
                "threshold": 1,
            },
            new_value={
                "method": "SSIM",
                "threshold": 10,
            },
        )
