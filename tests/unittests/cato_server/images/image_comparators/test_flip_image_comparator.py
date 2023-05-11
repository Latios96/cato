import os
import shutil
import tempfile
from unittest import mock

import pytest

from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_result import ComparisonResult
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.result_status import ResultStatus
from cato_server.images.image_comparators.flip_image_comparator import (
    FlipImageComparator,
)
from tests.unittests.cato_server.images.image_comparators.utils import (
    images_are_visually_equal,
    images_are_equal,
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
    image_comparator = FlipImageComparator()

    comparison_result = image_comparator.compare(
        reference_image,
        output_image,
        ComparisonSettings(threshold=0.0, method=ComparisonMethod.FLIP),
        str(tmpdir),
    )

    assert comparison_result == ComparisonResult(
        status=ResultStatus.FAILED,
        message="Images are not equal! FLIP mean error was 0.001, max threshold is 0.000",
        diff_image=str(
            tmpdir.join("diff_image_c04b964d-f443-4ae9-8b43-47fe6d2422d0.png")
        ),
        error=0.001431,
    )


@mock.patch("uuid.uuid4")
def test_compare_image_should_fail_waith_and_without_watermark(
    mock_uuid4, test_resource_provider, tmpdir
):
    mock_uuid4.return_value = "c04b964d-f443-4ae9-8b43-47fe6d2422d0"
    output_image = test_resource_provider.resource_by_name("with_watermark.png")
    reference_image = test_resource_provider.resource_by_name("without_watermark.png")
    image_comparator = FlipImageComparator()

    comparison_result = image_comparator.compare(
        reference_image,
        output_image,
        ComparisonSettings(threshold=0, method=ComparisonMethod.FLIP),
        str(tmpdir),
    )

    assert comparison_result == ComparisonResult(
        status=ResultStatus.FAILED,
        message="Images are not equal! FLIP mean error was 0.102, max threshold is 0.000",
        diff_image=tmpdir.join("diff_image_c04b964d-f443-4ae9-8b43-47fe6d2422d0.png"),
        error=0.102406,
    )
    assert images_are_visually_equal(
        comparison_result.diff_image,
        test_resource_provider.resource_by_name("with_watermark_diff_flip.png"),
        0.99,
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
        image_comparator = FlipImageComparator()

        comparison_result = image_comparator.compare(
            image,
            other_image,
            ComparisonSettings(threshold=0, method=ComparisonMethod.FLIP),
            str(tmpdir),
        )

        assert comparison_result == ComparisonResult(
            status=ResultStatus.SUCCESS,
            message=None,
            diff_image=tmpdir.join(
                "diff_image_c04b964d-f443-4ae9-8b43-47fe6d2422d0.png"
            ),
            error=0,
        )


@mock.patch("uuid.uuid4")
def test_compare_image_should_succeed_for_image_that_produced_NaN_score(
    mock_uuid4, test_resource_provider, tmpdir
):
    mock_uuid4.return_value = "c04b964d-f443-4ae9-8b43-47fe6d2422d0"
    image = test_resource_provider.resource_by_name("producedNaN.exr")
    with tempfile.TemporaryDirectory() as tmpdirname:
        other_image = os.path.join(tmpdirname, "producedNaN.exr")
        shutil.copy(image, other_image)
        image_comparator = FlipImageComparator()

        comparison_result = image_comparator.compare(
            image,
            other_image,
            ComparisonSettings(threshold=1, method=ComparisonMethod.FLIP),
            str(tmpdir),
        )

        assert comparison_result == ComparisonResult(
            status=ResultStatus.SUCCESS,
            message=None,
            diff_image=tmpdir.join(
                "diff_image_c04b964d-f443-4ae9-8b43-47fe6d2422d0.png"
            ),
            error=0.0,
        )


@mock.patch("uuid.uuid4")
def test_compare_image_should_fail_for_same_image_paths(
    mock_uuid4, test_resource_provider, tmpdir
):
    mock_uuid4.return_value = "c04b964d-f443-4ae9-8b43-47fe6d2422d0"
    image = test_resource_provider.resource_by_name("100x100_reference.png")
    image_comparator = FlipImageComparator()

    with pytest.raises(ValueError):
        comparison_result = image_comparator.compare(
            image,
            image,
            ComparisonSettings(threshold=1, method=ComparisonMethod.FLIP),
            str(tmpdir),
        )


def test_compare_image_should_fail_when_comparing_png_to_exr(tmpdir):
    image_comparator = FlipImageComparator()

    comparison_result = image_comparator.compare(
        "image.exr",
        "image.png",
        ComparisonSettings(threshold=1, method=ComparisonMethod.FLIP),
        str(tmpdir),
    )

    assert comparison_result == ComparisonResult(
        status=ResultStatus.FAILED,
        message=f"FLIP does not support comparison of reference .exr to output .png, image need to have same format.",
        diff_image=None,
        error=1,
    )


def test_compare_image_should_fail_when_comparing_exr_to_png(tmpdir):
    image_comparator = FlipImageComparator()

    comparison_result = image_comparator.compare(
        "image.png",
        "image.exr",
        ComparisonSettings(threshold=1, method=ComparisonMethod.FLIP),
        str(tmpdir),
    )

    assert comparison_result == ComparisonResult(
        status=ResultStatus.FAILED,
        message=f"FLIP does not support comparison of reference .png to output .exr, image need to have same format.",
        diff_image=None,
        error=1,
    )


@mock.patch("uuid.uuid4")
def test_compare_image_should_succeed_threshold_not_exceeded(
    mock_uuid4, test_resource_provider, tmpdir
):
    mock_uuid4.return_value = "c04b964d-f443-4ae9-8b43-47fe6d2422d0"
    output_image = test_resource_provider.resource_by_name("with_watermark.png")
    reference_image = test_resource_provider.resource_by_name("without_watermark.png")
    image_comparator = FlipImageComparator()

    comparison_result = image_comparator.compare(
        reference_image,
        output_image,
        ComparisonSettings(threshold=0.2, method=ComparisonMethod.FLIP),
        str(tmpdir),
    )

    assert comparison_result == ComparisonResult(
        status=ResultStatus.SUCCESS,
        message=None,
        diff_image=tmpdir.join("diff_image_c04b964d-f443-4ae9-8b43-47fe6d2422d0.png"),
        error=0.102406,
    )


@pytest.mark.parametrize(
    "image1_name,image2_name",
    [
        ("unsupported-file.txt", "other-unsupported-file.txt"),
    ],
)
def test_compare_image_should_fail_for_non_images(
    image1_name, image2_name, test_resource_provider, tmpdir
):
    image1 = test_resource_provider.resource_by_name(image1_name)
    image2 = test_resource_provider.resource_by_name(image2_name)
    image_comparator = FlipImageComparator()

    with pytest.raises(ValueError):
        comparison_result = image_comparator.compare(
            image1,
            image2,
            ComparisonSettings(threshold=1, method=ComparisonMethod.FLIP),
            str(tmpdir),
        )


@pytest.mark.parametrize(
    "image_name,extension",
    [
        ("png_8_bit", ".png"),
        ("png_16_bit", ".png"),
        ("exr_singlechannel_16_bit", ".exr"),
        ("exr_singlechannel_32_bit", ".exr"),
        ("transparent_red_over_opaque_blue", ".png"),
    ],
)
def test_compare_image_should_generate_diff_image_correctly(
    image_name, extension, test_resource_provider, tmpdir
):
    reference_image = test_resource_provider.resource_by_name(
        os.path.join("sphere_test_images", "reference", image_name + extension)
    )
    output_image = test_resource_provider.resource_by_name(
        os.path.join("sphere_test_images", "output", image_name + extension)
    )
    image_comparator = FlipImageComparator()

    comparison_result = image_comparator.compare(
        reference_image,
        output_image,
        ComparisonSettings(threshold=0, method=ComparisonMethod.FLIP),
        str(tmpdir),
    )

    assert comparison_result.status == ResultStatus.FAILED
    assert comparison_result.message.startswith(
        "Images are not equal! FLIP mean error "
    )
    expected_diff_image = test_resource_provider.resource_by_name(
        os.path.join("sphere_test_images", "expected_diff_flip", image_name + ".png")
    )
    assert images_are_visually_equal(
        comparison_result.diff_image, expected_diff_image, 0.97
    )
