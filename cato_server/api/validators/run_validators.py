from typing import Dict, List

from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.api.schemas.run_schemas import CreateFullRunSchema
from cato_server.api.validators.basic import SchemaValidator


class CreateFullRunValidator(SchemaValidator):
    def __init__(self, project_repository: ProjectRepository):
        super(CreateFullRunValidator, self).__init__(CreateFullRunSchema())
        self._project_repository = project_repository

    def validate(self, data: Dict) -> Dict[str, List[str]]:
        errors = super(CreateFullRunValidator, self).validate(data)

        project_id = data.get("project_id")
        if project_id and not self._project_repository.find_by_id(project_id):
            self.add_error(
                errors, "project_id", f"No project with id {project_id} exists!"
            )

        return errors
