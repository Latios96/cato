import os
import shutil
import tempfile
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import IO

import logging

from cato_server.domain.comparison_result import ComparisonResult
from cato_server.domain.comparison_settings import ComparisonSettings
from cato_server.images.image_comparator import ImageComparator
from cato_server.images.store_image import StoreImage

logger = logging.getLogger(__name__)


@dataclass
class CompareImageResult:
    result: ComparisonResult
    reference_image_id: int
    output_image_id: int


class CompareImage:
    def __init__(self, store_image: StoreImage, image_comparator: ImageComparator):
        self._store_image = store_image
        self._image_comparator = image_comparator

    def compare_image(
        self,
        output_image_file: IO,
        output_image_name: str,
        reference_image_file: IO,
        reference_image_name: str,
        comparison_settings: ComparisonSettings,
    ):
        with tempfile.TemporaryDirectory() as tmpdirname:
            output_image, output_image_path = self._store_image_in_db(
                tmpdirname, output_image_file, output_image_name
            )
            reference_image, reference_image_path = self._store_image_in_db(
                tmpdirname, reference_image_file, reference_image_name
            )

            result = self._image_comparator.compare(
                reference_image_path, output_image_path, comparison_settings
            )
            logger.debug("Deleting tmpdir %s", tmpdirname)

        return CompareImageResult(
            result=result,
            reference_image_id=reference_image.id,
            output_image_id=output_image.id,
        )

    def _store_image_in_db(self, tmpdirname, image_file: IO, image_name: str):
        tmp_path = Path(tmpdirname) / str(uuid.uuid4()) / image_name
        if not os.path.exists(tmp_path.parent):
            os.makedirs(tmp_path.parent)
        with open(tmp_path, "wb") as tmp:
            shutil.copyfileobj(image_file, tmp)
            logger.debug("Wrote image to temporary file")
        image = self._store_image.store_image(str(tmp_path))

        return image, str(tmp_path)
