import datetime

from cato.domain.comparison_settings import ComparisonSettings
from cato_server.domain.test_edit import (
    ComparisonSettingsEdit,
    ComparisonSettingsEditValue,
)
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

    def create_edit(
        self, test_result_id, comparison_settings: ComparisonSettings
    ) -> ComparisonSettingsEdit:
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

        logger.info("Comparing images..")
        result = self._compare_image.compare_image_from_db(
            output_image, reference_image, comparison_settings
        )
        logger.info("Compared images, test status is, error ")

        created_at = self._get_created_at()
        comparison_settings_edit = ComparisonSettingsEdit(
            id=0,
            test_id=test_result.id,
            created_at=created_at,
            old_value=ComparisonSettingsEditValue(
                comparison_settings=test_result.comparison_settings,
                status=test_result.status,
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

        saved_edit = self._test_edit_repository.save(comparison_settings_edit)

        test_result.diff_image = result.diff_image_id
        test_result.status = result.status
        test_result.message = result.message
        self._test_result_repository.save(test_result)

        return saved_edit

    def _get_created_at(self):
        return datetime.datetime.now()
