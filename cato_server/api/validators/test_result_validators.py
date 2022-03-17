from typing import List, Dict

from cato_server.api.schemas.test_result_schemas import (
    CreateOutputSchema,
    FinishTestResultSchema,
    StartTestResultSchema,
)
from cato_server.api.validators.basic import SchemaValidator
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.output_repository import OutputRepository
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)


class CreateOutputValidator(SchemaValidator):
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        output_repository: OutputRepository,
    ):
        super(CreateOutputValidator, self).__init__(CreateOutputSchema())
        self._test_result_repository = test_result_repository
        self._output_repository = output_repository

    def validate(self, data: Dict) -> Dict[str, List[str]]:
        errors = super(CreateOutputValidator, self).validate(data)

        test_result_id: int = data.get("testResultId")
        test_result = self._test_result_repository.find_by_id(test_result_id)
        existing_output = self._output_repository.find_by_test_result_id(test_result_id)
        if test_result_id and not test_result:
            self.add_error(
                errors,
                "testResultId",
                f"No test result exists for id {test_result_id}.",
            )
        elif test_result_id and existing_output:
            self.add_error(
                errors,
                "testResultId",
                f"An output already exists for test result with id {test_result_id}.",
            )

        return errors


class FinishTestResultValidator(SchemaValidator):
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        image_repository: ImageRepository,
    ):
        super(FinishTestResultValidator, self).__init__(FinishTestResultSchema())
        self._test_result_repository = test_result_repository
        self._image_repository = image_repository

    def validate(self, data: Dict) -> Dict[str, List[str]]:
        errors = super(FinishTestResultValidator, self).validate(data)

        test_result = self._test_result_repository.find_by_id(data.get("id"))
        if not test_result:
            self.add_error(
                errors, "id", f"No TestResult with id {data.get('id')} exists!"
            )

        image_output = data.get("imageOutput")
        if image_output and not self._image_repository.find_by_id(image_output):
            self.add_error(
                errors, "imageOutput", f"No image exists for id {image_output}."
            )

        reference_image = data.get("referenceImage")
        if reference_image and not self._image_repository.find_by_id(reference_image):
            self.add_error(
                errors, "referenceImage", f"No image exists for id {reference_image}."
            )

        diff_image = data.get("diffImage")
        if diff_image and not self._image_repository.find_by_id(diff_image):
            self.add_error(errors, "diffImage", f"No image exists for id {diff_image}.")

        if data.get("status") == "FAILED":
            if not data.get("failureReason"):
                self.add_error(
                    errors,
                    "failureReason",
                    "failureReason is required if test_status is 'FAILED'",
                )

        return errors


class StartTestResultValidator(SchemaValidator):
    def __init__(
        self,
        test_result_repository: TestResultRepository,
    ):
        super(StartTestResultValidator, self).__init__(StartTestResultSchema())
        self._test_result_repository = test_result_repository

    def validate(self, data: Dict) -> Dict[str, List[str]]:
        errors = super(StartTestResultValidator, self).validate(data)

        test_result = self._test_result_repository.find_by_id(data.get("id"))
        if not test_result:
            self.add_error(
                errors, "id", f"No TestResult with id {data.get('id')} exists!"
            )

        return errors
