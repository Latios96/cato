from typing import Dict

from cato_server.mappers.abstract_class_mapper import AbstractClassMapper
from cato_server.mappers.internal.test_status_value_mapper import TestStatusValueMapper
from cato_server.usecases.compare_image import CompareImageResult


class CompareImageResultClassMapper(AbstractClassMapper[CompareImageResult]):
    def __init__(self):
        self._test_status_value_mapper = TestStatusValueMapper()

    def map_from_dict(self, json_data: Dict) -> CompareImageResult:
        return CompareImageResult(
            status=json_data["status"],
            message=json_data.get("message"),
            reference_image_id=json_data["reference_image_id"],
            output_image_id=json_data["output_image_id"],
        )

    def map_to_dict(self, comparison_settings: CompareImageResult) -> Dict:
        return {
            "status": self._test_status_value_mapper.map_to(comparison_settings.status),
            "message": comparison_settings.message,
            "reference_image_id": comparison_settings.reference_image_id,
            "output_image_id": comparison_settings.output_image_id,
        }
