from typing import Dict

from cato_server.domain.test_identifier import TestIdentifier
from cato_server.mappers.abstract_class_mapper import AbstractClassMapper


class TestIdentifierClassMapper(AbstractClassMapper):
    def map_from_dict(self, json_data: Dict) -> TestIdentifier:
        return TestIdentifier(json_data["suite_name"], json_data["test_name"])

    def map_to_dict(self, test_result: TestIdentifier) -> Dict:
        return {
            "suite_name": test_result.suite_name,
            "test_name": test_result.test_name,
        }
