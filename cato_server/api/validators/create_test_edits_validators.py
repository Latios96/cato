from typing import Dict, List

from cato_server.api.schemas.create_test_edits_schemas import (
    CreateComparisonSettingsEditSchema,
    CreateReferenceImageSettingsEditSchema,
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

        test_result_id = data.get("testResultId")
        test_result = self._test_result_repository.find_by_id(test_result_id)
        if test_result_id and not test_result:
            self.add_error(
                errors,
                "id",
                f"No TestResult with id {data.get('testResultId')} exists!",
            )

        if test_result and not test_result.comparison_settings:
            self.add_error(
                errors,
                "comparisonSettings",
                "Can't edit a test result which has no comparison settings!",
            )

        return errors


class CreateReferenceImageEditValidator(SchemaValidator):
    def __init__(self, test_result_repository: TestResultRepository):
        super(CreateReferenceImageEditValidator, self).__init__(
            CreateReferenceImageSettingsEditSchema()
        )
        self._test_result_repository = test_result_repository

    def validate(self, data: Dict) -> Dict[str, List[str]]:
        errors = super(CreateReferenceImageEditValidator, self).validate(data)

        test_result_id = data.get("testResultId")
        test_result = self._test_result_repository.find_by_id(test_result_id)
        if test_result_id and not test_result:
            self.add_error(
                errors,
                "id",
                f"No TestResult with id {data.get('testResultId')} exists!",
            )

        if test_result and not test_result.image_output:
            self.add_error(
                errors,
                "testResultId",
                "Can't edit a test result which has no image output!",
            )

        if test_result and not test_result.comparison_settings:
            self.add_error(
                errors,
                "comparisonSettings",
                "Can't edit a test result which has no comparison settings!",
            )

        return errors
