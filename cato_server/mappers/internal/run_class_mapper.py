from typing import Dict

from cato_server.domain.run import Run
from cato_server.mappers.abstract_class_mapper import AbstractClassMapper
from cato_server.mappers.internal.datetime_value_mapper import DateTimeValueMapper


class RunClassMapper(AbstractClassMapper[Run]):
    def map_from_dict(self, json_data: Dict) -> Run:
        return Run(
            id=json_data["id"],
            project_id=json_data["project_id"],
            started_at=DateTimeValueMapper().map_from(json_data["started_at"]),
        )

    def map_to_dict(self, run: Run) -> Dict:
        return {
            "id": run.id,
            "project_id": run.project_id,
            "started_at": DateTimeValueMapper().map_to(run.started_at),
        }
