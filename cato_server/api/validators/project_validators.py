from typing import Dict, List

from cato.storage.abstract.project_repository import ProjectRepository
from cato_server.api.schemas.project_schemas import CreateProjectSchema
from cato_server.api.validators.basic import SchemaValidator


class CreateProjectValidator(SchemaValidator):
    def __init__(self, project_repository: ProjectRepository):
        super(CreateProjectValidator, self).__init__(CreateProjectSchema())
        self._project_repository = project_repository

    def validate(self, data: Dict) -> Dict[str, List[str]]:
        errors = super(CreateProjectValidator, self).validate(data)

        project_name = data.get("name")
        if project_name and self._project_repository.find_by_name(project_name):
            self.add_error(
                errors, "name", f'Project with name "{project_name}" already exists!'
            )

        return errors
