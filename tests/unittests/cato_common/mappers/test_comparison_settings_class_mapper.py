from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings


def test_map_from(object_mapper):
    result = object_mapper.from_dict(
        {"method": "SSIM", "threshold": 1}, ComparisonSettings
    )

    assert result == ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)


def test_map_to(object_mapper):
    result = object_mapper.to_dict(
        ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
    )

    assert result == {"method": "SSIM", "threshold": 1}
