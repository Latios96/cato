from typing import Dict, List

from cato.storage.abstract.run_repository import RunRepository
from cato.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.api.schemas.suite_result_schemas import CreateSuiteResultSchema
from cato_server.api.validators.basic import SchemaValidator


class CreateSuiteResultValidator(SchemaValidator):
    def __init__(
        self,
        run_repository: RunRepository,
        suite_result_repository=SuiteResultRepository,
    ):
        super(CreateSuiteResultValidator, self).__init__(CreateSuiteResultSchema())
        self._run_repository = run_repository
        self._suite_result_repository = suite_result_repository

    def validate(self, data: Dict) -> Dict[str, List[str]]:
        errors = super(CreateSuiteResultValidator, self).validate(data)

        run_id = data.get("run_id")
        if run_id and not self._run_repository.find_by_id(run_id):
            self.add_error(errors, "run_id", f"No run with id {run_id} exists.")

        suite_name = data.get("suite_name")
        if (
            suite_name
            and run_id
            and self._suite_result_repository.find_by_run_id_and_name(
                run_id, suite_name
            )
        ):
            self.add_error(
                errors,
                "suite_name",
                f'A test suite with name {data.get("suite_name")} already exists for run id {data["run_id"]}',
            )

        return errors
