from typing import Dict

from cato_server.domain.project import Project
from cato_server.mappers.abstract_class_mapper import AbstractClassMapper


class ProjectClassMapper(AbstractClassMapper[Project]):
    def map_from_dict(self, json_data: Dict) -> Project:
        return Project(json_data["id"], json_data["name"])

    def map_to_dict(self, project: Project) -> Dict:
        return {"id": project.id, "name": project.name}
