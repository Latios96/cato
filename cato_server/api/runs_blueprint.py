import logging
from http.client import BAD_REQUEST

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from cato_common.dtos.create_full_run_dto import CreateFullRunDto
from cato_common.mappers.object_mapper import ObjectMapper
from cato_common.mappers.page_mapper import PageMapper
from cato_common.storage.page import PageRequest, Page
from cato_server.api.filter_option_utils import run_filter_options_from_request
from cato_server.api.page_utils import (
    page_request_from_request,
)
from cato_server.api.validators.run_validators import (
    CreateFullRunValidator,
)
from cato_server.run_status_calculator import RunStatusCalculator
from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)
from cato_server.usecases.aggregate_run import AggregateRun
from cato_server.usecases.create_run import CreateRunUsecase

logger = logging.getLogger(__name__)


class RunsBlueprint(APIRouter):
    def __init__(
        self,
        run_repository: RunRepository,
        project_repository: ProjectRepository,
        test_result_repository: TestResultRepository,
        create_run_usecase: CreateRunUsecase,
        suite_result_repository: SuiteResultRepository,
        object_mapper: ObjectMapper,
        page_mapper: PageMapper,
        aggregate_run: AggregateRun,
    ):
        super(RunsBlueprint, self).__init__()
        self._run_repository = run_repository
        self._project_repository = project_repository
        self._test_result_repository = test_result_repository
        self._create_run_usecase = create_run_usecase
        self._suite_result_repository = suite_result_repository
        self._object_mapper = object_mapper
        self._page_mapper = page_mapper
        self._aggregate_run = aggregate_run

        self._run_status_calculator = RunStatusCalculator()

        self.get("/runs/project/{project_id}/aggregate")(self.aggregate_runs_by_project)
        self.get("/runs/project/{project_id}/branches")(self.get_branches)
        self.get("/runs/{run_id}/exists")(self.run_id_exists)
        self.get("/runs/{run_id}/aggregate")(self.aggregate_run)
        self.post("/runs")(self.create_run)

    def aggregate_runs_by_project(self, project_id: int, request: Request) -> Response:
        run_filter_options = run_filter_options_from_request(request.query_params)

        page_request = page_request_from_request(request.query_params)
        if not page_request:
            page_request = PageRequest.first(30)

        run_page = self._run_repository.find_by_project_id_with_paging(
            project_id, page_request, run_filter_options
        )
        aggregated_runs = self._aggregate_run.aggregate_runs_by_project_id(
            project_id, run_page.entities
        )
        aggregated_runs_page = Page(
            page_number=run_page.page_number,
            page_size=run_page.page_size,
            total_entity_count=run_page.total_entity_count,
            entities=aggregated_runs,
        )

        return JSONResponse(content=self._page_mapper.to_dict(aggregated_runs_page))

    def run_id_exists(self, run_id: int) -> Response:
        run = self._run_repository.find_by_id(run_id)
        if not run:
            return Response(status_code=404)

        return JSONResponse(content={"succes": True}, status_code=200)

    async def create_run(self, request: Request) -> Response:
        request_json = await request.json()
        errors = CreateFullRunValidator(self._project_repository).validate(request_json)
        if errors:
            return JSONResponse(content=errors, status_code=BAD_REQUEST)

        create_run_dto = self._object_mapper.from_dict(request_json, CreateFullRunDto)

        run = self._create_run_usecase.create_run(create_run_dto)
        return JSONResponse(content=self._object_mapper.to_dict(run), status_code=201)

    def aggregate_run(self, run_id: int) -> Response:
        run = self._run_repository.find_by_id(run_id)
        if not run:
            return Response(status_code=404)

        run_aggregates = self._aggregate_run.aggregate_runs_by_project_id(
            run.project_id, [run]
        )
        run_aggregate = run_aggregates[0]

        return JSONResponse(content=self._object_mapper.to_dict(run_aggregate))

    def get_branches(self, project_id: int) -> Response:
        branch_names = self._run_repository.find_branches_for_project(project_id)
        return JSONResponse(content=self._object_mapper.many_to_dict(branch_names))
