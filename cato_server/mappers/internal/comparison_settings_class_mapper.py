from typing import Dict

from cato.domain.comparison_settings import ComparisonSettings
from cato_server.mappers.abstract_class_mapper import AbstractClassMapper
from cato_server.mappers.internal.comparison_method_value_mapper import (
    ComparisonMethodValueMapper,
)


class ComparisonSettingsClassMapper(AbstractClassMapper[ComparisonSettings]):
    def __init__(self):
        self._comparison_method_value_mapper = ComparisonMethodValueMapper()

    def map_from_dict(self, json_data: Dict) -> ComparisonSettings:
        return ComparisonSettings(
            method=self._comparison_method_value_mapper.map_from(json_data["method"]),
            threshold=json_data["threshold"],
        )

    def map_to_dict(self, comparison_settings: ComparisonSettings) -> Dict:
        return {
            "method": self._comparison_method_value_mapper.map_to(
                comparison_settings.method
            ),
            "threshold": comparison_settings.threshold,
        }
