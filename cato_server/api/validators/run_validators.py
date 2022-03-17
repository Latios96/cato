from collections import Counter
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

        project_id = data.get("projectId")
        if project_id and not self._project_repository.find_by_id(project_id):
            self.add_error(
                errors, "projectId", f"No project with id {project_id} exists!"
            )

        if data.get("testSuites"):
            self._validate_suite_names_are_unique(errors, data.get("testSuites"))

            for test_suite in data.get("testSuites"):
                self._validate_test_names_are_unique(errors, test_suite)

        return errors

    def _validate_suite_names_are_unique(self, errors, test_suites):
        counter = Counter([x["suiteName"] for x in test_suites])
        duplicates = [item for item, count in counter.items() if count > 1]

        if duplicates:
            self.add_error(
                errors, "testSuites", "duplicate suite name(s): {}".format(duplicates)
            )

    def _validate_test_names_are_unique(self, errors, test_suite):
        counter = Counter([x["testName"] for x in test_suite["tests"]])
        duplicates = [item for item, count in counter.items() if count > 1]

        if duplicates:
            self.add_error(
                errors, "testResults", "duplicate test name(s): {}".format(duplicates)
            )
