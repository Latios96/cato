from typing import List, Dict

from cato.domain.test_identifier import TestIdentifier
from cato.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.api.schemas.test_result_schemas import CreateTestResultSchema
from cato_server.api.validators.basic import SchemaValidator


class CreateTestResultValidator(SchemaValidator):
    def __init__(
        self,
        suite_result_repository: SuiteResultRepository,
        file_storage: AbstractFileStorage,
    ):
        super(CreateTestResultValidator, self).__init__(CreateTestResultSchema())
        self._suite_result_repository = suite_result_repository
        self._file_storage = file_storage

    def validate(self, data: Dict) -> Dict[str, List[str]]:
        errors = super(CreateTestResultValidator, self).validate(data)

        suite_result_id = data.get("suite_result_id")
        suite_result = self._suite_result_repository.find_by_id(suite_result_id)
        if suite_result_id and not suite_result:
            self.add_error(
                errors,
                "suite_result_id",
                f"No suite result exists for id {suite_result_id}.",
            )

        test_identifier = data.get("test_identifier")
        if test_identifier and suite_result:
            expected_test_identifier = TestIdentifier(
                suite_result.suite_name, data.get("test_name")
            )
            if not expected_test_identifier == TestIdentifier.from_string(
                test_identifier
            ):
                self.add_error(
                    errors,
                    "test_identifier",
                    f"Provided {test_identifier} does not match suite name {suite_result.suite_name} of linked suite result and test name {data.get('test_name')}",
                )

        image_output = data.get("image_output")
        if image_output and not self._file_storage.find_by_id(image_output):
            self.add_error(
                errors, "image_output", f"No file exists for id {image_output}."
            )

        reference_image = data.get("reference_image")
        if reference_image and not self._file_storage.find_by_id(reference_image):
            self.add_error(
                errors, "reference_image", f"No file exists for id {reference_image}."
            )

        return errors
