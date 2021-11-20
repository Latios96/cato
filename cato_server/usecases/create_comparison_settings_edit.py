import datetime
from typing import Tuple, Optional

from cato.domain.comparison_settings import ComparisonSettings
from cato_common.domain.test_edit import (
    ComparisonSettingsEdit,
    ComparisonSettingsEditValue,
)
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.test_edit_repository import TestEditRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.compare_image import CompareImage

import logging

logger = logging.getLogger(__name__)


class CreateComparisonSettingsEdit:
    def __init__(
        self,
        test_edit_repository: TestEditRepository,
        test_result_repository: TestResultRepository,
        compare_image: CompareImage,
        image_repository: ImageRepository,
    ):
        self._test_edit_repository = test_edit_repository
        self._test_result_repository = test_result_repository
        self._compare_image = compare_image
        self._image_repository = image_repository

    def can_create_edit(self, test_result_id: int) -> Tuple[bool, Optional[str]]:
        try:
            self._validate_test_result_input(test_result_id)
            return True, None
        except ValueError as e:
            return False, str(e)

    def create_edit(
        self, test_result_id, comparison_settings: ComparisonSettings
    ) -> ComparisonSettingsEdit:
        output_image, reference_image, test_result = self._validate_test_result_input(
            test_result_id
        )

        logger.info("Comparing images..")
        result = self._compare_image.compare_image_from_db(
            output_image, reference_image, comparison_settings
        )
        logger.info(
            "Compared images, test status is %s, error %s", result.status, result.error
        )

        created_at = self._get_created_at()
        comparison_settings_edit = self._create_comparison_edit(
            comparison_settings, created_at, result, test_result
        )

        saved_edit = self._test_edit_repository.save(comparison_settings_edit)

        test_result.comparison_settings = comparison_settings
        test_result.diff_image = result.diff_image_id
        test_result.unified_test_status = UnifiedTestStatus(result.status.value)
        test_result.message = result.message
        self._test_result_repository.save(test_result)

        logger.info(
            "Created comparison settings edit with id %s for test result with id %s ",
            saved_edit.id,
            test_result_id,
        )

        return saved_edit

    def _validate_test_result_input(self, test_result_id):
        test_result = self._test_result_repository.find_by_id(test_result_id)
        if not test_result:
            raise ValueError(f"Could not find a test result with id {test_result_id}")

        if not test_result.comparison_settings:
            raise ValueError(
                "Can't edit a test result which has no comparison settings!"
            )

        output_image = self._image_repository.find_by_id(test_result.image_output)
        if not output_image:
            raise ValueError("Can not edit test result with no output image!")
        reference_image = self._image_repository.find_by_id(test_result.reference_image)
        if not reference_image:
            raise ValueError("Can not edit test result with no reference image!")
        return output_image, reference_image, test_result

    def _create_comparison_edit(
        self, comparison_settings, created_at, result, test_result
    ):
        return ComparisonSettingsEdit(
            id=0,
            test_id=test_result.id,
            test_identifier=test_result.test_identifier,
            created_at=created_at,
            old_value=ComparisonSettingsEditValue(
                comparison_settings=test_result.comparison_settings,
                status=test_result.unified_test_status.to_result_status(),
                message=test_result.message,
                diff_image_id=test_result.diff_image,
                error_value=test_result.error_value,
            ),
            new_value=ComparisonSettingsEditValue(
                comparison_settings=comparison_settings,
                status=result.status,
                message=result.message,
                diff_image_id=result.diff_image_id,
                error_value=result.error,
            ),
        )

    def _get_created_at(self):
        return datetime.datetime.now()
