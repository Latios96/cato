from typing import Dict, List

from cato_server.api.schemas.create_test_edits_schemas import (
    CreateComparisonSettingsEditSchema,
)
from cato_server.api.validators.basic import SchemaValidator
from cato_server.storage.abstract.test_result_repository import TestResultRepository


class CreateComparisonSettingsEditValidator(SchemaValidator):
    def __init__(self, test_result_repository: TestResultRepository):
        super(CreateComparisonSettingsEditValidator, self).__init__(
            CreateComparisonSettingsEditSchema()
        )
        self._test_result_repository = test_result_repository

    def validate(self, data: Dict) -> Dict[str, List[str]]:
        errors = super(CreateComparisonSettingsEditValidator, self).validate(data)

        test_result_id = data.get("test_result_id")
        if test_result_id and not self._test_result_repository.find_by_id(
            test_result_id
        ):
            self.add_error(
                errors,
                "id",
                f"No TestResult with id {data.get('test_result_id')} exists!",
            )

        return errors
