import logging
import os
import uuid
from typing import Optional

import numpy
from PIL import Image

from cato_common.domain.comparison_result import ComparisonResult
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.result_status import ResultStatus

logger = logging.getLogger(__name__)
from flip_evaluator import flip_python_api


class FlipImageComparator:
    def compare(
        self,
        reference: str,
        output: str,
        comparison_settings: ComparisonSettings,
        workdir: str,
    ) -> ComparisonResult:
        reference_and_output_are_the_same = os.path.abspath(
            reference
        ) == os.path.abspath(output)
        if reference_and_output_are_the_same:
            raise ValueError(
                f"Images to compare need to be different, pointing to same path: {os.path.abspath(reference)}"
            )

        same_format_error = self._verify_images_have_same_format(reference, output)
        if same_format_error:
            return ComparisonResult(
                status=ResultStatus.FAILED,
                message=same_format_error,
                diff_image=None,
                error=1,
            )

        not_supported_format_error = self._verify_images_have_supported_format(
            reference, output
        )
        if not_supported_format_error:
            return ComparisonResult(
                status=ResultStatus.FAILED,
                message=not_supported_format_error,
                diff_image=None,
                error=1,
            )

        # todo check resolution errors
        try:
            diff_image_np, mean_error, stats = flip_python_api.evaluate(
                reference,
                output,
                "HDR" if reference.endswith(".exr") else "LDR",
                parameters={},
            )
        except Exception as e:
            message = str(e)
            message = message.replace("\n", " ")
            return ComparisonResult(
                status=ResultStatus.FAILED,
                message=f"FLIP: {message}",
                diff_image=None,
                error=0,
            )
        if diff_image_np.shape[0] == 0 or diff_image_np.shape[1] == 0:
            raise ValueError("Could not read images!")

        diff_image_path = os.path.join(workdir, f"diff_image_{uuid.uuid4()}.png")
        diff_image = Image.fromarray(numpy.uint8(diff_image_np * 255))
        diff_image.save(diff_image_path)

        mean_error = round(mean_error, 6)

        if mean_error > comparison_settings.threshold:
            return ComparisonResult(
                status=ResultStatus.FAILED,
                message=f"Images are not equal! FLIP mean error was {mean_error:.3f}, max threshold is {comparison_settings.threshold:.3f}",
                diff_image=diff_image_path,
                error=mean_error,
            )

        return ComparisonResult(
            status=ResultStatus.SUCCESS,
            message=None,
            diff_image=diff_image_path,
            error=mean_error,
        )

    def _verify_images_have_same_format(
        self, reference: str, output: str
    ) -> Optional[str]:
        reference_image_extension = os.path.splitext(reference)[1]
        output_image_extension = os.path.splitext(output)[1]

        if reference_image_extension != output_image_extension:
            return f"FLIP does not support comparison of reference {reference_image_extension} to output {output_image_extension}, image need to have same format."

    def _verify_images_have_supported_format(
        self, reference: str, output: str
    ) -> Optional[str]:
        reference_image_extension = os.path.splitext(reference)[1]
        output_image_extension = os.path.splitext(output)[1]
        if reference_image_extension not in {".png", ".exr"}:
            return f"FLIP does not support comparison of images with format {output_image_extension}. Only .png and .exr are supported."
        if reference_image_extension not in {".png", ".exr"}:
            return f"FLIP does not support comparison of images with format {output_image_extension}. Only .png and .exr are supported."
