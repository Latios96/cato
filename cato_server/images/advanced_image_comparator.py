import logging
import os.path
import uuid

import cv2
import numpy
from skimage import metrics

from cato.domain.test_status import TestStatus
from cato_server.domain.comparison_result import ComparisonResult
from cato_server.domain.comparison_settings import ComparisonSettings
from cato_server.domain.resolution import Resolution

logger = logging.getLogger(__name__)


class AdvancedImageComparator:
    def compare(
        self,
        reference: str,
        output: str,
        comparison_settings: ComparisonSettings,
        workdir: str,
    ) -> ComparisonResult:
        reference_output = os.path.abspath(reference) == os.path.abspath(output)
        if reference_output:
            raise ValueError(
                f"Images to compare need to be different, pointing to same path: {os.path.abspath(reference)}"
            )
        logger.debug("Reading images")
        output_image = cv2.imread(output, cv2.IMREAD_COLOR | cv2.IMREAD_ANYDEPTH)
        if output_image is None:
            raise ValueError(
                f"Could not read image from {output}, unsupported file format!"
            )
        reference_image = cv2.imread(reference, cv2.IMREAD_COLOR | cv2.IMREAD_ANYDEPTH)
        if reference_image is None:
            raise ValueError(
                f"Could not read image from {reference}, unsupported file format!"
            )

        output_image_resolution = Resolution(
            output_image.shape[0], output_image.shape[1]
        )
        reference_image_resolution = Resolution(
            reference_image.shape[0], reference_image.shape[1]
        )

        images_have_same_resolution = (
            output_image_resolution == reference_image_resolution
        )
        logger.debug(
            "Images have same resolution: %s",
            "yes" if images_have_same_resolution else "no",
        )
        if not images_have_same_resolution:
            return ComparisonResult(
                status=TestStatus.FAILED,
                message=f"Images have different resolutions! Reference image is {reference_image_resolution}, output image is {output_image_resolution}",
                diff_image=None,
            )

        (score, diff) = metrics.structural_similarity(
            reference_image, output_image, full=True, multichannel=True
        )
        logger.debug("SSIM score: %s ", score)
        diff = (diff * 255).astype("uint8")

        diff_image = self._create_diff_image(
            output_image, diff, comparison_settings.threshold, workdir
        )

        if score < comparison_settings.threshold:
            return ComparisonResult(
                status=TestStatus.FAILED,
                message=f"Images are not equal! {comparison_settings.method} score was {score:.3f}, max threshold is {comparison_settings.threshold:.3f}",
                diff_image=diff_image,
            )

        return ComparisonResult(
            status=TestStatus.SUCCESS, message=None, diff_image=diff_image
        )

    def _create_diff_image(
        self,
        output_image: numpy.array,
        diff: numpy.array,
        threshold: float,
        workdir: str,
    ) -> str:
        is_linear = output_image.dtype == "float32"
        diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        diff_gray = ~diff_gray

        int_threshold = 255 - int(threshold * 255)
        thresh = cv2.threshold(diff_gray.copy(), threshold, 1, cv2.THRESH_TOZERO)[1]
        thresh = cv2.threshold(thresh, 0, 1, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

        black_channel = numpy.ones(thresh.shape, dtype=thresh.dtype)
        weighted_green = cv2.merge((black_channel, thresh, black_channel))
        if is_linear:
            output_image = output_image.clip(0, 1)
            output_image = lin2srgb(output_image)
            output_image *= 255
        output_image = output_image.astype("uint8")
        output_with_highlights = cv2.addWeighted(
            output_image, 1, cv2.merge((thresh, thresh, thresh)), -1, 0
        )
        output_with_highlights = cv2.addWeighted(
            output_with_highlights, 1, weighted_green, 1, 0
        )
        target_path = os.path.join(workdir, f"diff_image_{uuid.uuid4()}.png")
        cv2.imwrite(target_path, output_with_highlights)

        return target_path


def lin2srgb(x):
    a = 0.055
    return numpy.where(x <= 0.0031308, x * 12.92, (1 + a) * numpy.power(x, 1 / 2.4) - a)
