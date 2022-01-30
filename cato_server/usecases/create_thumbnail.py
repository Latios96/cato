import os
import tempfile
import uuid
from typing import Optional

from cato_common.domain.test_result import TestResult
from cato_server.images.oiio_binaries_discovery import OiioBinariesDiscovery
from cato_server.images.oiio_command_executor import OiioCommandExecutor
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository

import logging

logger = logging.getLogger(__name__)


class CreateThumbnail:
    def __init__(
        self,
        image_repository: ImageRepository,
        file_storage: AbstractFileStorage,
        oiio_binaries_discovery: OiioBinariesDiscovery,
        test_result_repository: TestResultRepository,
        oiio_command_executor: OiioCommandExecutor,
    ):
        self._image_repository = image_repository
        self._file_storage = file_storage
        self._oiio_binaries_discovery = oiio_binaries_discovery
        self._test_result_repository = test_result_repository
        self._oiio_command_executor = oiio_command_executor

    def create_thumbnail(self, test_result: TestResult) -> None:
        image_id = self._resolve_image_id(test_result)
        if not image_id:
            raise ValueError(f"Test result has no images!")
        image = self._image_repository.find_by_id(image_id)
        if not image:
            raise ValueError(f"No Image found with id {image_id}")
        file = self._file_storage.find_by_id(image.original_file_id)
        if not file:
            raise ValueError(f"No File found with id {image.original_file_id}")
        input_file_path = self._file_storage.get_path(file)

        with tempfile.TemporaryDirectory() as tmpdirname:
            thumbnail_target_path = os.path.join(
                tmpdirname, f"thumbnail_{uuid.uuid4()}.png"
            )
            command = f"{self._oiio_binaries_discovery.get_oiiotool_executable()} -i {input_file_path} --resize 0x75 -o {thumbnail_target_path}"
            self._oiio_command_executor.execute_command(command)
            if not os.path.exists(thumbnail_target_path):
                raise RuntimeError(
                    f"No thumbnail was created at path {thumbnail_target_path}"
                )
            thumbnail_file = self._file_storage.save_file(thumbnail_target_path)

        test_result.thumbnail_file_id = thumbnail_file.id
        self._test_result_repository.save(test_result)
        logger.info(
            "Created thumbnail with file id %s for test result with id %s",
            thumbnail_file.id,
            test_result.id,
        )

    def _resolve_image_id(self, test_result: TestResult) -> Optional[int]:
        if test_result.reference_image:
            return test_result.reference_image
        if test_result.image_output:
            return test_result.image_output
        return None
