import os
import shutil
import tempfile
from unittest import mock

import pytest
from PIL import ImageChops
from PIL import Image

from cato.domain.test_status import TestStatus
from cato_server.domain.comparison_method import ComparisonMethod
from cato_server.domain.comparison_result import ComparisonResult
from cato_server.domain.comparison_settings import ComparisonSettings
from cato_server.images.advanced_image_comparator import AdvancedImageComparator


def test_compare_image_should_fail_different_resolution(test_resource_provider, tmpdir):
    output_image = test_resource_provider.resource_by_name("100x100_reference.png")
    reference_image = test_resource_provider.resource_by_name("200x100_reference.png")
    image_comparator = AdvancedImageComparator()

    comparison_result = image_comparator.compare(
        reference_image,
        output_image,
        ComparisonSettings(threshold=1, method=ComparisonMethod.SSIM),
        str(tmpdir),
    )

    assert comparison_result == ComparisonResult(
        status=TestStatus.FAILED,
        message="Images have different resolutions! Reference image is 100x200px, output image is 100x100px",
        diff_image=None,
    )


@mock.patch("uuid.uuid4")
def test_compare_image_should_fail_one_pixel_different(
    mock_uuid4, test_resource_provider, tmpdir
):
    mock_uuid4.return_value = "c04b964d-f443-4ae9-8b43-47fe6d2422d0"
    output_image = test_resource_provider.resource_by_name("single_pixel_output.png")
    reference_image = test_resource_provider.resource_by_name(
        "single_pixel_reference.png"
    )
    image_comparator = AdvancedImageComparator()

    comparison_result = image_comparator.compare(
        reference_image,
        output_image,
        ComparisonSettings(threshold=1, method=ComparisonMethod.SSIM),
        str(tmpdir),
    )

    assert comparison_result == ComparisonResult(
        status=TestStatus.FAILED,
        message="Images are not equal! ComparisonMethod.SSIM score was 0.994, max threshold is 1.000",
        diff_image=tmpdir.join("diff_image_c04b964d-f443-4ae9-8b43-47fe6d2422d0.png"),
    )


def images_are_equal(image1, image2):
    image_one = Image.open(image1)
    image_two = Image.open(image2)
    diff = ImageChops.difference(image_one, image_two)
    if diff.getbbox():
        return False
    return True


@mock.patch("uuid.uuid4")
def test_compare_image_should_fail_waith_and_without_watermark(
    mock_uuid4, test_resource_provider, tmpdir
):
    mock_uuid4.return_value = "c04b964d-f443-4ae9-8b43-47fe6d2422d0"
    output_image = test_resource_provider.resource_by_name("with_watermark.png")
    reference_image = test_resource_provider.resource_by_name("without_watermark.png")
    image_comparator = AdvancedImageComparator()

    comparison_result = image_comparator.compare(
        reference_image,
        output_image,
        ComparisonSettings(threshold=1, method=ComparisonMethod.SSIM),
        str(tmpdir),
    )

    assert comparison_result == ComparisonResult(
        status=TestStatus.FAILED,
        message="Images are not equal! ComparisonMethod.SSIM score was 0.885, max threshold is 1.000",
        diff_image=tmpdir.join("diff_image_c04b964d-f443-4ae9-8b43-47fe6d2422d0.png"),
    )
    assert images_are_equal(
        comparison_result.diff_image,
        test_resource_provider.resource_by_name("with_watermark_diff.png"),
    )


@mock.patch("uuid.uuid4")
def test_compare_image_should_succeed_same_image(
    mock_uuid4, test_resource_provider, tmpdir
):
    mock_uuid4.return_value = "c04b964d-f443-4ae9-8b43-47fe6d2422d0"
    image = test_resource_provider.resource_by_name("100x100_reference.png")
    with tempfile.TemporaryDirectory() as tmpdirname:
        other_image = os.path.join(tmpdirname, "100x100_reference.png")
        shutil.copy(image, other_image)
        image_comparator = AdvancedImageComparator()

        comparison_result = image_comparator.compare(
            image,
            other_image,
            ComparisonSettings(threshold=1, method=ComparisonMethod.SSIM),
            str(tmpdir),
        )

        assert comparison_result == ComparisonResult(
            status=TestStatus.SUCCESS,
            message=None,
            diff_image=tmpdir.join(
                "diff_image_c04b964d-f443-4ae9-8b43-47fe6d2422d0.png"
            ),
        )


@mock.patch("uuid.uuid4")
def test_compare_image_should_fail_for_same_image_paths(
    mock_uuid4, test_resource_provider, tmpdir
):
    mock_uuid4.return_value = "c04b964d-f443-4ae9-8b43-47fe6d2422d0"
    image = test_resource_provider.resource_by_name("100x100_reference.png")
    image_comparator = AdvancedImageComparator()

    with pytest.raises(ValueError):
        comparison_result = image_comparator.compare(
            image,
            image,
            ComparisonSettings(threshold=1, method=ComparisonMethod.SSIM),
            str(tmpdir),
        )


@mock.patch("uuid.uuid4")
def test_compare_image_should_succeed_threshold_not_exceeded(
    mock_uuid4, test_resource_provider, tmpdir
):
    mock_uuid4.return_value = "c04b964d-f443-4ae9-8b43-47fe6d2422d0"
    output_image = test_resource_provider.resource_by_name("with_watermark.png")
    reference_image = test_resource_provider.resource_by_name("without_watermark.png")
    image_comparator = AdvancedImageComparator()

    comparison_result = image_comparator.compare(
        reference_image,
        output_image,
        ComparisonSettings(threshold=0.8, method=ComparisonMethod.SSIM),
        str(tmpdir),
    )

    assert comparison_result == ComparisonResult(
        status=TestStatus.SUCCESS,
        message=None,
        diff_image=tmpdir.join("diff_image_c04b964d-f443-4ae9-8b43-47fe6d2422d0.png"),
    )


@pytest.mark.parametrize(
    "image1_name,image2_name",
    [
        ("unsupported-file.txt", "alembic-config-for-tests.ini"),
        ("with_watermark.png", "unsupported-file.txt"),
        ("unsupported-file.txt", "with_watermark.png"),
    ],
)
def test_compare_image_should_fail_for_non_images(
    image1_name, image2_name, test_resource_provider, tmpdir
):
    image1 = test_resource_provider.resource_by_name(image1_name)
    image2 = test_resource_provider.resource_by_name(image2_name)
    image_comparator = AdvancedImageComparator()

    with pytest.raises(ValueError):
        comparison_result = image_comparator.compare(
            image1,
            image2,
            ComparisonSettings(threshold=1, method=ComparisonMethod.SSIM),
            str(tmpdir),
        )
