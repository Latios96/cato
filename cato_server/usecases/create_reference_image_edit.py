import datetime
from typing import Tuple, Optional

from cato_common.domain.image import Image
from cato_common.domain.test_result import TestResult
from cato_server.domain.test_edit import ReferenceImageEdit, ReferenceImageEditValue
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.test_edit_repository import TestEditRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.compare_image import CompareImage

import logging

logger = logging.getLogger(__name__)


class CreateReferenceImageEdit:
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

    def create_edit(self, test_result_id: int) -> ReferenceImageEdit:
        image_output, test_result = self._validate_test_result_input(test_result_id)

        logger.info("Comparing images..")
        result = self._compare_image.compare_image_from_db(
            image_output, image_output, test_result.comparison_settings
        )
        logger.info(
            "Compared images, test status is %s, error %s", result.status, result.error
        )

        created_at = self._get_created_at()
        reference_image_edit = ReferenceImageEdit(
            id=0,
            test_id=test_result.id,
            created_at=created_at,
            old_value=ReferenceImageEditValue(
                reference_image_id=test_result.reference_image,
                diff_image_id=test_result.diff_image,
                error_value=test_result.error_value,
                status=test_result.status,
                message=test_result.message,
            ),
            new_value=ReferenceImageEditValue(
                reference_image_id=image_output.id,
                diff_image_id=result.diff_image_id,
                error_value=result.error,
                status=result.status,
                message=result.message,
            ),
        )

        saved_edit = self._test_edit_repository.save(reference_image_edit)

        test_result.reference_image = test_result.image_output
        test_result.diff_image = result.diff_image_id
        test_result.status = result.status
        test_result.message = result.message
        self._test_result_repository.save(test_result)

        return saved_edit

    def _validate_test_result_input(
        self, test_result_id: int
    ) -> Tuple[Image, TestResult]:
        test_result = self._test_result_repository.find_by_id(test_result_id)
        if not test_result:
            raise ValueError(f"Could not find a test result with id {test_result_id}")

        if not test_result.image_output:
            raise ValueError("Can't edit a test result which has no image_output!")
        image_output = self._image_repository.find_by_id(test_result.image_output)
        return image_output, test_result

    def _get_created_at(self):
        return datetime.datetime.now()
