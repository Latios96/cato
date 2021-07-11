import os
import shutil
import tempfile

import pytest

from cato.domain.test_status import TestStatus
from cato_server.domain.comparison_method import ComparisonMethod
from cato_server.domain.comparison_result import ComparisonResult
from cato_server.domain.comparison_settings import ComparisonSettings
from cato_server.images.advanced_image_comparator import AdvancedImageComparator


def test_compare_image_should_fail_different_resolution(test_resource_provider):
    output_image = test_resource_provider.resource_by_name("100x100_reference.png")
    reference_image = test_resource_provider.resource_by_name("200x100_reference.png")
    image_comparator = AdvancedImageComparator()

    comparison_result = image_comparator.compare(
        reference_image,
        output_image,
        ComparisonSettings(threshold=1, method=ComparisonMethod.SSIM),
    )

    assert comparison_result == ComparisonResult(
        status=TestStatus.FAILED,
        message="Images have different resolutions! Reference image is 100x200px, output image is 100x100px",
        diff_image=None,
    )


def test_compare_image_should_fail_one_pixel_different(test_resource_provider):
    output_image = test_resource_provider.resource_by_name("single_pixel_output.png")
    reference_image = test_resource_provider.resource_by_name(
        "single_pixel_reference.png"
    )
    image_comparator = AdvancedImageComparator()

    comparison_result = image_comparator.compare(
        reference_image,
        output_image,
        ComparisonSettings(threshold=1, method=ComparisonMethod.SSIM),
    )

    assert comparison_result == ComparisonResult(
        status=TestStatus.FAILED,
        message="Images are not equal! ComparisonMethod.SSIM score was 0.994, max threshold is 1.000",
        diff_image=None,
    )


def test_compare_image_should_fail_waith_and_without_watermark(test_resource_provider):
    output_image = test_resource_provider.resource_by_name("with_watermark.png")
    reference_image = test_resource_provider.resource_by_name("without_watermark.png")
    image_comparator = AdvancedImageComparator()

    comparison_result = image_comparator.compare(
        reference_image,
        output_image,
        ComparisonSettings(threshold=1, method=ComparisonMethod.SSIM),
    )

    assert comparison_result == ComparisonResult(
        status=TestStatus.FAILED,
        message="Images are not equal! ComparisonMethod.SSIM score was 0.885, max threshold is 1.000",
        diff_image=None,
    )


def test_compare_image_should_succeed_same_image(test_resource_provider):
    image = test_resource_provider.resource_by_name("100x100_reference.png")
    with tempfile.TemporaryDirectory() as tmpdirname:
        other_image = os.path.join(tmpdirname, "100x100_reference.png")
        shutil.copy(image, other_image)
        image_comparator = AdvancedImageComparator()

        comparison_result = image_comparator.compare(
            image,
            other_image,
            ComparisonSettings(threshold=1, method=ComparisonMethod.SSIM),
        )

        assert comparison_result == ComparisonResult(
            status=TestStatus.SUCCESS, message=None, diff_image=None
        )


def test_compare_image_should_fail_for_same_image_paths(test_resource_provider):
    image = test_resource_provider.resource_by_name("100x100_reference.png")
    image_comparator = AdvancedImageComparator()

    with pytest.raises(ValueError):
        comparison_result = image_comparator.compare(
            image, image, ComparisonSettings(threshold=1, method=ComparisonMethod.SSIM)
        )


def test_compare_image_should_succeed_threshold_not_exceeded(test_resource_provider):
    output_image = test_resource_provider.resource_by_name("with_watermark.png")
    reference_image = test_resource_provider.resource_by_name("without_watermark.png")
    image_comparator = AdvancedImageComparator()

    comparison_result = image_comparator.compare(
        reference_image,
        output_image,
        ComparisonSettings(threshold=0.8, method=ComparisonMethod.SSIM),
    )

    assert comparison_result == ComparisonResult(
        status=TestStatus.SUCCESS,
        message=None,
        diff_image=None,
    )
