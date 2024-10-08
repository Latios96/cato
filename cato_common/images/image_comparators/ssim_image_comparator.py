import logging
import math
import os.path
import uuid

# https://github.com/opencv/opencv/issues/21326
import os

os.environ["OPENCV_IO_ENABLE_OPENEXR"] = "1"

import cv2
import numpy
from skimage import metrics
from PIL import Image, ImageOps
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.comparison_result import ComparisonResult
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.resolution import Resolution

logger = logging.getLogger(__name__)


class SsimImageComparator:
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
        logger.debug("Reading images")
        output_image = self._read_image(output)
        if output_image is None:
            raise ValueError(
                f"Could not read image from {output}, unsupported file format!"
            )
        reference_image = self._read_image(reference)
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
                status=ResultStatus.FAILED,
                message=f"Images have different resolutions! Reference image is {reference_image_resolution}, output image is {output_image_resolution}",
                diff_image=None,
                error=0,
            )

        output_image = self._normalize_image(output_image)
        reference_image = self._normalize_image(reference_image)

        (score, diff) = metrics.structural_similarity(
            reference_image, output_image, full=True, channel_axis=-1
        )
        score = float(score)
        if math.isnan(score):
            score = 1
        logger.debug("SSIM score: %s ", score)
        diff = diff.astype("float32")

        file_extension = os.path.splitext(output)[1]
        is_linear = file_extension == ".exr"
        diff_image = self._create_diff_image(output_image, diff, workdir, is_linear)

        if score < comparison_settings.threshold:
            return ComparisonResult(
                status=ResultStatus.FAILED,
                message=f"Images are not equal! {comparison_settings.method} score was {score:.3f}, max threshold is {comparison_settings.threshold:.3f}",
                diff_image=diff_image,
                error=score,
            )

        return ComparisonResult(
            status=ResultStatus.SUCCESS,
            message=None,
            diff_image=diff_image,
            error=score,
        )

    def _read_image(self, image_path):
        is_tiff = (
            os.path.splitext(image_path)[1] == ".tif"
            or os.path.splitext(image_path)[1] == ".tiff"
        )
        if is_tiff:
            image = cv2.imread(image_path, cv2.IMREAD_COLOR)
            return cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        return cv2.imread(image_path, cv2.IMREAD_UNCHANGED | cv2.IMREAD_ANYDEPTH)

    def _create_diff_image(
        self,
        output_image: numpy.array,
        diff: numpy.array,
        workdir: str,
        is_linear: bool,
    ) -> str:
        heatmap = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        heatmap = cv2.applyColorMap(
            ~(heatmap.clip(0, 1) * 255).astype("uint8"), cv2.COLORMAP_WINTER
        )
        heatmap = Image.fromarray(
            cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGBA), mode="RGBA"
        )

        diff = Image.fromarray(
            (cv2.cvtColor(diff, cv2.COLOR_BGR2RGBA).clip(0, 1) * 255).astype("uint8"),
            mode="RGBA",
        )

        output_image = output_image.clip(0, 1)
        if is_linear:
            output_image = lin2srgb(output_image)
        output_image *= 255
        output_image = Image.fromarray(
            cv2.cvtColor(output_image, cv2.COLOR_BGR2RGBA).astype("uint8"), mode="RGBA"
        )

        diff_image_as_luminance = diff.convert("L")
        diff_image_as_luminance = ImageOps.invert(diff_image_as_luminance)
        (diff_luminance,) = diff_image_as_luminance.split()
        l_thresholded = diff_luminance.point(lambda p: 0 if p > 1 else 255)

        composited_diff_image = Image.composite(output_image, heatmap, l_thresholded)
        target_path = os.path.join(workdir, f"diff_image_{uuid.uuid4()}.png")
        composited_diff_image.save(target_path)
        return target_path

    def _normalize_image(self, image):
        if image.dtype == "uint8":
            image = image.astype("float32")
            image /= 255.0
            return image
        elif image.dtype == "uint16":
            image = image.astype("float32")
            image /= 65535
            return image
        elif image.dtype == "float32":
            return image


def lin2srgb(x):
    a = 0.055
    return numpy.where(x <= 0.0031308, x * 12.92, (1 + a) * numpy.power(x, 1 / 2.4) - a)
