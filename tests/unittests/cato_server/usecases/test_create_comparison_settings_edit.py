import datetime
from unittest import mock

import pytest

from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings
from cato_server.domain.test_edit import (
    ComparisonSettingsEdit,
    ComparisonSettingsEditValue,
)
from cato_server.storage.abstract.test_edit_repository import TestEditRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.create_comparison_settings_edit import (
    CreateComparisonSettingsEdit,
)
from tests.utils import mock_safe


def test_create_edit_with_success(test_result_factory):
    test_edit_repository = mock_safe(TestEditRepository)
    test_edit_repository.save.side_effect = lambda x: x
    test_result_repository = mock_safe(TestResultRepository)
    test_result_repository.find_by_id.return_value = test_result_factory(
        id=5,
        comparison_settings=ComparisonSettings(
            method=ComparisonMethod.SSIM, threshold=1
        ),
    )
    create_comparison_settings_edit = CreateComparisonSettingsEdit(
        test_edit_repository, test_result_repository
    )
    created_at = datetime.datetime(year=2021, month=9, day=17)
    create_comparison_settings_edit._get_created_at = lambda: created_at

    edit = create_comparison_settings_edit.create_edit(
        1, ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
    )

    assert edit == ComparisonSettingsEdit(
        id=0,
        test_id=5,
        created_at=created_at,
        old_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1
            )
        ),
        new_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1
            )
        ),
    )


def test_no_test_with_id_found():
    test_edit_repository = mock_safe(TestEditRepository)
    test_result_repository = mock_safe(TestResultRepository)
    test_result_repository.find_by_id.return_value = None
    create_comparison_settings_edit = CreateComparisonSettingsEdit(
        test_edit_repository, test_result_repository
    )

    with pytest.raises(ValueError):
        create_comparison_settings_edit.create_edit(
            1, ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
        )


def test_test_with_no_comparison_settings(test_result_factory):
    test_edit_repository = mock_safe(TestEditRepository)
    test_result_repository = mock_safe(TestResultRepository)
    test_result_repository.find_by_id.return_value = test_result_factory(
        id=5,
    )
    create_comparison_settings_edit = CreateComparisonSettingsEdit(
        test_edit_repository, test_result_repository
    )

    with pytest.raises(ValueError):
        create_comparison_settings_edit.create_edit(
            1, ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
        )
