from http.client import BAD_REQUEST, CREATED

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import Response, JSONResponse

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.api.dtos.test_edit_count import TestEditCount
from cato_server.api.validators.create_test_edits_validators import (
    CreateComparisonSettingsEditValidator,
    CreateReferenceImageEditValidator,
)
from cato_server.storage.abstract.test_edit_repository import TestEditRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.create_comparison_settings_edit import (
    CreateComparisonSettingsEdit,
)
from cato_server.usecases.create_reference_image_edit import CreateReferenceImageEdit


class TestEditBlueprint(APIRouter):
    def __init__(
        self,
        test_edit_repository: TestEditRepository,
        test_result_repository: TestResultRepository,
        object_mapper: ObjectMapper,
        create_comparison_settings_edit: CreateComparisonSettingsEdit,
        create_reference_image_edit: CreateReferenceImageEdit,
    ):
        super(TestEditBlueprint, self).__init__()
        self._test_edit_repository = test_edit_repository
        self._object_mapper = object_mapper
        self._test_result_repository = test_result_repository
        self._create_comparison_settings_edit = create_comparison_settings_edit
        self._create_reference_image_edit = create_reference_image_edit

        self.get("/test_edits/{test_result_id}")(self.test_edits_by_test_result_id)
        self.get("/test_edits/can-edit/{test_result_id}/comparison_settings")(
            self.can_edit_comparison_settings
        )
        self.get("/test_edits/can-edit/{test_result_id}/reference_image")(
            self.can_edit_reference_image
        )
        self.get("/test_edits/runs/{run_id}")(self.test_edits_by_run_id)
        self.get("/test_edits/runs/{run_id}/edits-to-sync")(
            self.test_edits_to_sync_by_run_id
        )
        self.get("/test_edits/runs/{run_id}/edits-to-sync-count")(
            self.has_edits_to_sync_by_run_id
        )
        self.post("/test_edits/comparison_settings")(
            self.create_comparison_settings_edit
        )
        self.post("/test_edits/reference_image")(self.create_reference_image_edit)

    def test_edits_by_test_result_id(self, test_result_id: int) -> Response:
        edits = self._test_edit_repository.find_by_test_id(test_result_id)

        return JSONResponse(content=self._object_mapper.many_to_dict(edits))

    def can_edit_comparison_settings(
        self,
        test_result_id: int,
    ) -> Response:
        can_be_edited = self._create_comparison_settings_edit.can_be_edited(
            test_result_id
        )

        return JSONResponse(content=self._object_mapper.to_dict(can_be_edited))

    def can_edit_reference_image(
        self,
        test_result_id: int,
    ) -> Response:
        can_be_edited = self._create_reference_image_edit.can_be_edited(test_result_id)

        return JSONResponse(content=self._object_mapper.to_dict(can_be_edited))

    def test_edits_by_run_id(self, run_id: int) -> Response:
        edits = self._test_edit_repository.find_by_run_id(run_id)

        return JSONResponse(content=self._object_mapper.many_to_dict(edits))

    def test_edits_to_sync_by_run_id(self, run_id: int) -> Response:
        edits = self._test_edit_repository.find_edits_to_sync_by_run_id(run_id)

        return JSONResponse(content=self._object_mapper.many_to_dict(edits))

    def has_edits_to_sync_by_run_id(self, run_id: int) -> Response:
        result = self._test_edit_repository.edits_to_sync_by_run_id_count(run_id)

        return JSONResponse(self._object_mapper.to_dict(TestEditCount(count=result)))

    async def create_comparison_settings_edit(self, request: Request) -> Response:
        request_json = await request.json()
        errors = CreateComparisonSettingsEditValidator(
            self._test_result_repository
        ).validate(request_json)
        if errors:
            return JSONResponse(content=errors, status_code=BAD_REQUEST)

        test_result_id = request_json["testResultId"]
        comparison_settings = self._object_mapper.from_dict(
            request_json["newValue"], ComparisonSettings
        )

        edit = self._create_comparison_settings_edit.create_edit(
            test_result_id, comparison_settings
        )

        return JSONResponse(
            content=self._object_mapper.to_dict(edit), status_code=CREATED
        )

    async def create_reference_image_edit(self, request: Request) -> Response:
        request_json = await request.json()
        errors = CreateReferenceImageEditValidator(
            self._test_result_repository
        ).validate(request_json)
        if errors:
            return JSONResponse(content=errors, status_code=BAD_REQUEST)

        test_result_id = request_json["testResultId"]

        edit = self._create_reference_image_edit.create_edit(test_result_id)

        return JSONResponse(
            content=self._object_mapper.to_dict(edit), status_code=CREATED
        )
