import logging
import os
import shutil
import tempfile
import uuid
from pathlib import Path
from typing import IO, Tuple

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.compare_image_result import CompareImageResult
from cato_common.domain.image import Image
from cato_server.images.advanced_image_comparator import AdvancedImageComparator
from cato_server.images.store_image import StoreImage
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage

logger = logging.getLogger(__name__)


class CompareImage:
    def __init__(
        self,
        store_image: StoreImage,
        advanced_image_comparator: AdvancedImageComparator,
        file_storage: AbstractFileStorage,
    ):
        self._store_image = store_image
        self._advanced_image_comparator = advanced_image_comparator
        self._file_storage = file_storage

    def compare_image(
        self,
        output_image_file: IO,
        output_image_name: str,
        reference_image_file: IO,
        reference_image_name: str,
        comparison_settings: ComparisonSettings,
    ) -> CompareImageResult:
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_image, output_image_path = self._store_image_in_db(
                tmpdirname, output_image_file, output_image_name
            )
            reference_image, reference_image_path = self._store_image_in_db(
                tmpdirname, reference_image_file, reference_image_name
            )

            result = self._advanced_image_comparator.compare(
                reference_image_path, output_image_path, comparison_settings, tmpdirname
            )

            stored_diff_image = self._store_image.store_image(result.diff_image)

            logger.debug("Deleting tmpdir %s", tmpdirname)

        return CompareImageResult(
            status=result.status,
            message=result.message,
            reference_image_id=reference_image.id,
            output_image_id=output_image.id,
            diff_image_id=stored_diff_image.id,
            error=result.error,
        )

    def compare_image_from_db(
        self,
        output_image: Image,
        reference_image: Image,
        comparison_settings: ComparisonSettings,
    ) -> CompareImageResult:
        with tempfile.TemporaryDirectory() as tmpdirname:
            original_output_image_file = self._file_storage.find_by_id(
                output_image.original_file_id
            )
            if not original_output_image_file:
                raise ValueError(
                    f"Can not compare images, found no file for original image file id {output_image.original_file_id}"
                )
            output_image_path = self._store_image_on_disk(
                tmpdirname,
                self._file_storage.get_read_stream(original_output_image_file),
                output_image.name,
            )

            reference_image_image_file = self._file_storage.find_by_id(
                reference_image.original_file_id
            )
            if not reference_image_image_file:
                raise ValueError(
                    f"Can not compare images, found no file for original image file id {reference_image.original_file_id}"
                )

            reference_image_path = self._store_image_on_disk(
                tmpdirname,
                self._file_storage.get_read_stream(reference_image_image_file),
                reference_image.name,
            )

            result = self._advanced_image_comparator.compare(
                reference_image_path, output_image_path, comparison_settings, tmpdirname
            )

            stored_diff_image = self._store_image.store_image(result.diff_image)

            logger.debug("Deleting tmpdir %s", tmpdirname)

        return CompareImageResult(
            status=result.status,
            message=result.message,
            reference_image_id=reference_image.id,
            output_image_id=output_image.id,
            diff_image_id=stored_diff_image.id,
            error=result.error,
        )

    def _store_image_in_db(
        self, tmpdirname: str, image_file: IO, image_name: str
    ) -> Tuple[Image, str]:
        tmp_path = self._store_image_on_disk(tmpdirname, image_file, image_name)
        image = self._store_image.store_image(tmp_path)

        return image, tmp_path

    def _store_image_on_disk(self, tmpdirname, image_file, image_name):
        tmp_path = Path(tmpdirname) / str(uuid.uuid4()) / image_name
        if not os.path.exists(tmp_path.parent):
            os.makedirs(tmp_path.parent)
        with open(tmp_path, "wb") as tmp:
            shutil.copyfileobj(image_file, tmp)
            logger.debug("Wrote image to temporary file")
        return str(tmp_path)
