import os

from cato.image_comparison.image_comparator import ImageComparator


def image_fixture(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), name)


def test_compare_success():
    comparator = ImageComparator()

    result = comparator.compare(
        image_fixture("test_image_white.png"), image_fixture("test_image_white.png")
    )

    assert not result.error


def test_compare_error():
    comparator = ImageComparator()

    result = comparator.compare(
        image_fixture("test_image_white.png"),
        image_fixture("test_image_white_one_black_pixel.png"),
    )

    assert result.error
    assert result.nwarn == 1


def test_compare_fail():
    comparator = ImageComparator()

    result = comparator.compare(
        image_fixture("test_image_white.png"), image_fixture("test_image_black.png")
    )

    assert result.error
