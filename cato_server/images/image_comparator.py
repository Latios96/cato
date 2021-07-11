import cv2
from skimage import metrics

from cato.domain.test_status import TestStatus
from cato_server.domain.comparison_settings import ComparisonSettings
from cato_server.domain.comparison_result import ComparisonResult
from cato_server.domain.resolution import Resolution


class ImageComparator:
    def compare(
        self, reference: str, output: str, comparison_settings: ComparisonSettings
    ) -> ComparisonResult:
        output_image = cv2.imread(output)
        reference_image = cv2.imread(reference)

        output_image_resolution = Resolution(
            output_image.shape[0], output_image.shape[1]
        )
        reference_image_resolution = Resolution(
            reference_image.shape[0], reference_image.shape[1]
        )

        images_have_same_resolution = (
            output_image_resolution == reference_image_resolution
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
        diff = (diff * 255).astype("uint8")

        if score < comparison_settings.threshold:
            return ComparisonResult(
                status=TestStatus.FAILED,
                message=f"Images are not equal! {comparison_settings.method} score was {score:.3f}, max threshold is {comparison_settings.threshold:.3f}",
                diff_image=None,
            )

        return ComparisonResult(
            status=TestStatus.SUCCESS, message=None, diff_image=None
        )
