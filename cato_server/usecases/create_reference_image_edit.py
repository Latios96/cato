import logging
from typing import Tuple, cast

from cato_common.domain.can_be_edited import CanBeEdited
from cato_common.domain.image import Image
from cato_common.domain.test_edit import ReferenceImageEdit, ReferenceImageEditValue
from cato_common.domain.test_result import TestResult
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.utils.typing import safe_unwrap
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.test_edit_repository import TestEditRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.task_queue.cato_celery import CatoCelery
from cato_server.usecases.compare_image import CompareImage
from cato_common.utils.datetime_utils import aware_now_in_utc

logger = logging.getLogger(__name__)


class CreateReferenceImageEdit:
    def __init__(
        self,
        test_edit_repository: TestEditRepository,
        test_result_repository: TestResultRepository,
        compare_image: CompareImage,
        image_repository: ImageRepository,
        cato_celery: CatoCelery,
    ):
        self._test_edit_repository = test_edit_repository
        self._test_result_repository = test_result_repository
        self._compare_image = compare_image
        self._image_repository = image_repository
        self._cato_celery = cato_celery

    def can_be_edited(self, test_result_id: int) -> CanBeEdited:
        try:
            self._validate_test_result_input(test_result_id)
            return CanBeEdited.yes()
        except ValueError as e:
            return CanBeEdited.no(str(e))

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
            test_identifier=test_result.test_identifier,
            created_at=created_at,
            old_value=ReferenceImageEditValue(
                reference_image_id=test_result.reference_image,
                diff_image_id=test_result.diff_image,
                error_value=test_result.error_value,
                status=test_result.unified_test_status.to_result_status(),
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
        test_result.unified_test_status = UnifiedTestStatus.from_result_status(
            result.status
        )
        test_result.error_value = result.error
        test_result.message = result.message
        self._test_result_repository.save(test_result)

        logger.info(
            "Created reference image edit with id %s for test result with id %s ",
            saved_edit.id,
            test_result_id,
        )

        try:
            self._cato_celery.launch_create_thumbnail_task(test_result.id)
        except Exception as e:
            logger.error(
                "Error when launching thumbnail task for test result with id %s, test result won't have a thumbnail:",
                test_result_id,
            )
            logger.exception(e)

        return cast(ReferenceImageEdit, saved_edit)

    def _validate_test_result_input(
        self, test_result_id: int
    ) -> Tuple[Image, TestResult]:
        test_result = self._test_result_repository.find_by_id(test_result_id)
        if not test_result:
            raise ValueError(f"Could not find a test result with id {test_result_id}")

        if not test_result.image_output:
            raise ValueError("Can't edit a test result which has no image_output!")

        if not test_result.comparison_settings:
            raise ValueError(
                "Can't edit a test result which has no comparison settings!"
            )

        image_output = safe_unwrap(
            self._image_repository.find_by_id(test_result.image_output)
        )
        return image_output, test_result

    def _get_created_at(self):
        return aware_now_in_utc()
