from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings
from cato_server.mappers.internal.comparison_settings_class_mapper import (
    ComparisonSettingsClassMapper,
)


def test_map_from():
    mapper = ComparisonSettingsClassMapper()

    result = mapper.map_from_dict({"method": "SSIM", "threshold": 1})

    assert result == ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)


def test_map_to():
    mapper = ComparisonSettingsClassMapper()

    result = mapper.map_to_dict(
        ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1)
    )

    assert result == {"method": "SSIM", "threshold": 1}
