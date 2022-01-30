import logging
from http.client import BAD_REQUEST

from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from cato_api_models.catoapimodels import (
    RunDto,
    RunStatusDto,
    RunSummaryDto,
    CreateFullRunDto,
)
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
from cato_server.storage.abstract.run_filter_options import RunFilterOptions
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)
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
    ):
        super(RunsBlueprint, self).__init__()
        self._run_repository = run_repository
        self._project_repository = project_repository
        self._test_result_repository = test_result_repository
        self._create_run_usecase = create_run_usecase
        self._suite_result_repository = suite_result_repository
        self._object_mapper = object_mapper
        self._page_mapper = page_mapper

        self._run_status_calculator = RunStatusCalculator()

        self.get("/runs/project/{project_id}")(self.runs_by_project)
        self.get("/runs/{run_id}/exists")(self.run_id_exists)
        self.post("/runs/full")(self.create_run)
        self.get("/runs/{run_id}/status")(self.status)
        self.get("/runs/{run_id}/summary")(self.summary)
        self.get("/runs/project/{project_id}/branches")(self.get_branches)

    def runs_by_project(self, project_id: int, request: Request) -> Response:
        page_request = page_request_from_request(request.query_params)
        run_filter_options = run_filter_options_from_request(request.query_params)
        if page_request:
            return self.runs_by_project_paged(
                project_id, page_request, run_filter_options
            )
        runs = self._run_repository.find_by_project_id(project_id)
        status_by_run_id = self._test_result_repository.find_status_by_project_id(
            project_id
        )
        duration_by_run_id = self._test_result_repository.duration_by_run_ids(
            {x.id for x in runs}
        )
        run_dtos = []
        for run in runs:
            status = self._run_status_calculator.calculate(
                status_by_run_id.get(run.id, set())
            )
            run_dtos.append(
                RunDto(
                    id=run.id,
                    project_id=run.id,
                    started_at=run.started_at.isoformat(),
                    status=RunStatusDto(status),
                    duration=duration_by_run_id[run.id],
                    branch_name=run.branch_name.name,
                )
            )
        return JSONResponse(content=self._object_mapper.many_to_dict(run_dtos))

    def runs_by_project_paged(
        self,
        project_id: int,
        page_request: PageRequest,
        run_filter_options: RunFilterOptions,
    ) -> Response:
        run_page = self._run_repository.find_by_project_id_with_paging(
            project_id, page_request, run_filter_options
        )
        status_by_run_id = self._test_result_repository.find_status_by_project_id(
            project_id
        )
        duration_by_run_id = self._test_result_repository.duration_by_run_ids(
            {x.id for x in run_page.entities}
        )
        run_dtos = []
        for run in run_page.entities:
            status = self._run_status_calculator.calculate(
                status_by_run_id.get(run.id, set())
            )
            run_dtos.append(
                RunDto(
                    id=run.id,
                    project_id=run.id,
                    started_at=run.started_at.isoformat(),
                    status=RunStatusDto(status),
                    duration=duration_by_run_id[run.id],
                    branch_name=run.branch_name.name,
                )
            )
        page = Page(
            page_number=page_request.page_number,
            page_size=page_request.page_size,
            total_entity_count=run_page.total_entity_count,
            entities=run_dtos,
        )
        return JSONResponse(content=self._page_mapper.to_dict(page))

    def run_id_exists(self, run_id: int) -> Response:
        run = self._run_repository.find_by_id(run_id)
        if not run:
            return Response(status_code=404)

        return JSONResponse(content={"succes": True}, status_code=200)

    def status(self, run_id: int) -> Response:
        status_by_run_id = self._test_result_repository.find_status_by_run_ids({run_id})

        if not status_by_run_id.get(run_id):
            return Response(status_code=404)

        return JSONResponse(
            content={
                "status": RunStatusCalculator()
                .calculate(status_by_run_id.get(run_id))
                .name
            }
        )

    async def create_run(self, request: Request) -> Response:
        request_json = await request.json()
        errors = CreateFullRunValidator(self._project_repository).validate(request_json)
        if errors:
            return JSONResponse(content=errors, status_code=BAD_REQUEST)

        create_run_dto = self._object_mapper.from_dict(request_json, CreateFullRunDto)

        run = self._create_run_usecase.create_run(create_run_dto)
        return JSONResponse(content=self._object_mapper.to_dict(run), status_code=201)

    def summary(self, run_id: int) -> Response:
        run = self._run_repository.find_by_id(run_id)
        if not run:
            return Response(status_code=404)
        status_by_run_id = self._test_result_repository.find_status_by_project_id(
            run.project_id
        )
        status = self._run_status_calculator.calculate(
            status_by_run_id.get(run.id, set())
        )
        duration = self._test_result_repository.duration_by_run_id(run_id)
        run_dto = RunDto(
            id=run.id,
            project_id=run.id,
            started_at=run.started_at.isoformat(),
            status=RunStatusDto(status),
            duration=duration,
            branch_name=run.branch_name.name,
        )
        suite_count = self._suite_result_repository.suite_count_by_run_id(run_id)
        test_count = self._test_result_repository.test_count_by_run_id(run_id)
        test_result_status_information = (
            self._test_result_repository.status_information_by_run_id(run_id)
        )

        run_summary_dto = RunSummaryDto(
            run=run_dto,
            suite_count=suite_count,
            test_count=test_count,
            waiting_test_count=test_result_status_information.not_started,
            running_test_count=test_result_status_information.running,
            succeeded_test_count=test_result_status_information.success,
            failed_test_count=test_result_status_information.failed,
        )
        return JSONResponse(content=self._object_mapper.to_dict(run_summary_dto))

    def get_branches(self, project_id: int) -> Response:
        branch_names = self._run_repository.find_branches_for_project(project_id)
        return JSONResponse(content=self._object_mapper.many_to_dict(branch_names))
