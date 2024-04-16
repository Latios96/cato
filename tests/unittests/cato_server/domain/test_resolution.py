import pytest

from cato_common.domain.resolution import Resolution


def test_to_string():
    resolution = Resolution(800, 600)

    assert str(resolution) == "800x600px"


@pytest.mark.parametrize("width,height", [(-1, 10), (10, -1), (-1, -1)])
def test_create_invalid_size(width, height):
    with pytest.raises(ValueError):
        Resolution(width, height)


def test_create_from_non_int():
    with pytest.raises(TypeError):
        Resolution("1", "1")
