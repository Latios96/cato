import os

from cato.image_utils.image_comparator import ImageComparator

TEST_IMAGE_WHITE_PNG = "test_image_white.png"


def test_compare_success(test_resource_provider):
    comparator = ImageComparator()

    result = comparator.compare(
        test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG),
        test_resource_provider.resource_by_name(TEST_IMAGE_WHITE_PNG),
    )

    assert not result.error


def test_compare_error(test_resource_provider):
    comparator = ImageComparator()

    result = comparator.compare(
        test_resource_provider.resource_by_name("test_image_white.png"),
        test_resource_provider.resource_by_name("test_image_white_one_black_pixel.png"),
    )

    assert result.error
    assert result.nwarn == 1


def test_compare_fail(test_resource_provider):
    comparator = ImageComparator()

    result = comparator.compare(
        test_resource_provider.resource_by_name("test_image_white.png"),
        test_resource_provider.resource_by_name("test_image_black.png"),
    )

    assert result.error
