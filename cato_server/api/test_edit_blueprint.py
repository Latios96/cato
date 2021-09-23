from http.client import BAD_REQUEST, CREATED

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from cato.domain.comparison_settings import ComparisonSettings
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.api.validators.create_test_edits_validators import (
    CreateComparisonSettingsEditValidator,
)
from cato_server.storage.abstract.test_edit_repository import TestEditRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.create_comparison_settings_edit import (
    CreateComparisonSettingsEdit,
)


class TestEditBlueprint(APIRouter):
    def __init__(
        self,
        test_edit_repository: TestEditRepository,
        test_result_repository: TestResultRepository,
        object_mapper: ObjectMapper,
        create_comparison_settings_edit: CreateComparisonSettingsEdit,
    ):
        super(TestEditBlueprint, self).__init__()
        self._test_edit_repository = test_edit_repository
        self._object_mapper = object_mapper
        self._test_result_repository = test_result_repository
        self._create_comparison_settings_edit = create_comparison_settings_edit

        self.get("/test_edits/{test_result_id}")(self.test_edits_by_test_result_id)
        self.get("/test_edits/runs/{run_id}")(self.test_edits_by_run_id)
        self.post("/test_edits/comparison_settings")(
            self.create_comparison_settings_edit
        )

    def test_edits_by_test_result_id(
        self, test_result_id: int, request: Request
    ) -> Response:
        edits = self._test_edit_repository.find_by_test_id(test_result_id)

        return JSONResponse(content=self._object_mapper.many_to_dict(edits))

    def test_edits_by_run_id(self, run_id: int, request: Request) -> Response:
        edits = self._test_edit_repository.find_by_run_id(run_id)

        return JSONResponse(content=self._object_mapper.many_to_dict(edits))

    async def create_comparison_settings_edit(self, request: Request) -> Response:
        request_json = await request.json()
        errors = CreateComparisonSettingsEditValidator(
            self._test_result_repository
        ).validate(request_json)
        if errors:
            return JSONResponse(content=errors, status_code=BAD_REQUEST)

        test_result_id = request_json["test_result_id"]
        comparison_settings = self._object_mapper.from_dict(
            request_json["new_value"], ComparisonSettings
        )

        edit = self._create_comparison_settings_edit.create_edit(
            test_result_id, comparison_settings
        )

        return JSONResponse(
            content=self._object_mapper.to_dict(edit), status_code=CREATED
        )