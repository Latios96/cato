from typing import Dict

from cato.config.config_file_parser import JsonConfigParser
from cato.config.config_file_writer import ConfigFileWriter
from cato.domain.config import Config
from cato_server.mappers.abstract_class_mapper import AbstractClassMapper
from cato_server.domain.submission_info import SubmissionInfo


class SubmissionInfoClassMapper(AbstractClassMapper[SubmissionInfo]):
    def map_from_dict(self, json_data: Dict) -> SubmissionInfo:
        return SubmissionInfo(
            config=self._map_config_from_dict(json_data["config"]),
            run_id=json_data["run_id"],
            resource_path=json_data["resource_path"],
            executable=json_data["executable"],
        )

    def map_to_dict(self, submission_info: SubmissionInfo) -> Dict:
        return {
            "config": self._map_config_to_dict(submission_info.config),
            "run_id": submission_info.run_id,
            "resource_path": submission_info.resource_path,
            "executable": submission_info.executable,
        }

    def _map_config_from_dict(self, json_data: Dict):
        return JsonConfigParser().parse_dict(json_data)

    def _map_config_to_dict(self, config: Config):
        return ConfigFileWriter().write_to_dict(config)
