from typing import Dict

from cato_server.mappers.abstract_class_mapper import AbstractClassMapper
from cato_server.domain.suite_result import SuiteResult


class SuiteResultClassMapper(AbstractClassMapper[SuiteResult]):
    def map_from_dict(self, json_data: Dict) -> SuiteResult:
        return SuiteResult(
            id=json_data["id"],
            run_id=json_data["run_id"],
            suite_name=json_data["suite_name"],
            suite_variables=json_data["suite_variables"],
        )

    def map_to_dict(self, suite_result: SuiteResult) -> Dict:
        return {
            "id": suite_result.id,
            "run_id": suite_result.run_id,
            "suite_name": suite_result.suite_name,
            "suite_variables": suite_result.suite_variables,
        }
