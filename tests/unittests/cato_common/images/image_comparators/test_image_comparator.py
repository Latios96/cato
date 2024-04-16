import pytest

from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.images.image_comparators.flip_image_comparator import (
    FlipImageComparator,
)
from cato_common.images.image_comparators.image_comparator import ImageComparator
from cato_common.images.image_comparators.ssim_image_comparator import (
    SsimImageComparator,
)
from tests.utils import mock_safe


@pytest.fixture
def comparator_fixture():
    ssim_image_comparator = mock_safe(SsimImageComparator)
    flip_image_comparator = mock_safe(FlipImageComparator)
    image_comparator = ImageComparator(ssim_image_comparator, flip_image_comparator)
    return image_comparator, ssim_image_comparator, flip_image_comparator


def test_compare_ssim(comparator_fixture):
    image_comparator, ssim_image_comparator, flip_image_comparator = comparator_fixture

    image_comparator.compare(
        "reference.png",
        "output.png",
        ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1),
        "workdir",
    )

    ssim_image_comparator.compare.assert_called_with(
        "reference.png",
        "output.png",
        ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1),
        "workdir",
    )


def test_compare_flip(comparator_fixture):
    image_comparator, ssim_image_comparator, flip_image_comparator = comparator_fixture

    image_comparator.compare(
        "reference.png",
        "output.png",
        ComparisonSettings(method=ComparisonMethod.FLIP, threshold=1),
        "workdir",
    )

    flip_image_comparator.compare.assert_called_with(
        "reference.png",
        "output.png",
        ComparisonSettings(method=ComparisonMethod.FLIP, threshold=1),
        "workdir",
    )
