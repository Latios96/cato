from typing import Dict, List

from cato_server.api.schemas.test_submission_schemas import SubmissionInfoSchema
from cato_server.api.validators.basic import SchemaValidator
from cato_server.storage.abstract.run_repository import RunRepository


class SubmissionInfoValidator(SchemaValidator):
    def __init__(self, run_repository: RunRepository):
        super(SubmissionInfoValidator, self).__init__(SubmissionInfoSchema())
        self._run_repository = run_repository

    def validate(self, data: Dict) -> Dict[str, List[str]]:
        errors = super(SubmissionInfoValidator, self).validate(data)
        run_id = data.get("run_id")
        run = self._run_repository.find_by_id(run_id)
        if run_id and not run:
            self.add_error(
                errors,
                "run_id",
                f"No run exists for id {run_id}.",
            )

        return errors
