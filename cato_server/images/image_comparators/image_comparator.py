from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_result import ComparisonResult
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_server.images.image_comparators.flip_image_comparator import (
    FlipImageComparator,
)
from cato_server.images.image_comparators.ssim_image_comparator import (
    SsimImageComparator,
)


class ImageComparator:
    def __init__(
        self,
        ssim_image_comparator: SsimImageComparator,
        flip_image_comparator: FlipImageComparator,
    ):
        self._ssim_image_comparator = ssim_image_comparator
        self._flip_image_comparator = flip_image_comparator

    def compare(
        self,
        reference: str,
        output: str,
        comparison_settings: ComparisonSettings,
        workdir: str,
    ) -> ComparisonResult:
        if comparison_settings.method == ComparisonMethod.SSIM:
            return self._ssim_image_comparator.compare(
                reference, output, comparison_settings, workdir
            )
        elif comparison_settings.method == ComparisonMethod.FLIP:
            return self._flip_image_comparator.compare(
                reference, output, comparison_settings, workdir
            )
        raise ValueError(f"Method {comparison_settings.method} is not supported.")
