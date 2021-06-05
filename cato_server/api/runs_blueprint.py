import logging
from http.client import BAD_REQUEST

import flask
from dateutil.parser import parse
from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from cato_api_models.catoapimodels import (
    RunDto,
    RunStatusDto,
    RunSummaryDto,
    CreateFullRunDto,
)
from cato_server.api.page_utils import page_request_from_request
from cato_server.api.utils import format_sse
from cato_server.api.validators.run_validators import (
    CreateRunValidator,
    CreateFullRunValidator,
)
from cato_server.configuration.optional_component import OptionalComponent
from cato_server.domain.run import Run
from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.mappers.page_mapper import PageMapper
from cato_server.queues.abstract_message_queue import AbstractMessageQueue
from cato_server.run_status_calculator import RunStatusCalculator
from cato_server.storage.abstract.page import PageRequest, Page
from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)
from cato_server.usecases.create_full_run import CreateFullRunUsecase

logger = logging.getLogger(__name__)


class RunsBlueprint(APIRouter):
    def __init__(
        self,
        run_repository: RunRepository,
        project_repository: ProjectRepository,
        test_result_repository: TestResultRepository,
        create_full_run_usecase: CreateFullRunUsecase,
        message_queue: OptionalComponent[AbstractMessageQueue],
        suite_result_repository: SuiteResultRepository,
        object_mapper: ObjectMapper,
        page_mapper: PageMapper,
    ):
        super(RunsBlueprint, self).__init__()
        self._run_repository = run_repository
        self._project_repository = project_repository
        self._test_result_repository = test_result_repository
        self._create_full_run_usecase = create_full_run_usecase
        self._message_queue = message_queue
        self._suite_result_repository = suite_result_repository
        self._object_mapper = object_mapper
        self._page_mapper = page_mapper

        self._run_status_calculator = RunStatusCalculator()

        self.get("/runs/project/{project_id}")(self.runs_by_project)
        self.get("/runs/{run_id}/exists")(self.run_id_exists)
        self.post("/runs")(self.create_run)
        self.post("/runs/full")(self.create_full_run)
        self.get("/runs/{run_id}/status")(self.status)
        self.get("/runs/{run_id}/summary")(self.summary)

        if self._message_queue.is_available():
            logger.info("Message queue is available, adding run events route")
            self.route("/runs/events/<int:project_id>", methods=["GET"])(
                self.run_events_for_project
            )

    def runs_by_project(self, project_id: int, request: Request):
        page_request = page_request_from_request(request.query_params)
        if page_request:
            return self.runs_by_project_paged(project_id, page_request)
        runs = self._run_repository.find_by_project_id(project_id)
        status_by_run_id = (
            self._test_result_repository.find_execution_status_by_project_id(project_id)
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
                )
            )
        return JSONResponse(content=self._object_mapper.many_to_dict(run_dtos))

    def runs_by_project_paged(self, project_id: int, page_request: PageRequest):
        run_page = self._run_repository.find_by_project_id_with_paging(
            project_id, page_request
        )
        status_by_run_id = (
            self._test_result_repository.find_execution_status_by_project_id(project_id)
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
                )
            )
        page = Page(
            page_number=page_request.page_number,
            page_size=page_request.page_size,
            total_entity_count=run_page.total_entity_count,
            entities=run_dtos,
        )
        return JSONResponse(content=self._page_mapper.to_dict(page))

    def run_id_exists(self, run_id):
        run = self._run_repository.find_by_id(run_id)
        if not run:
            return Response(status_code=404)

        return JSONResponse(content={"succes": True}, status_code=200)

    async def create_run(self, request: Request):
        request_json = await request.json()
        errors = CreateRunValidator(self._project_repository).validate(request_json)
        if errors:
            return JSONResponse(content=errors, status_code=BAD_REQUEST)

        run = Run(
            id=0,
            project_id=request_json["project_id"],
            started_at=parse(request_json["started_at"]),
        )
        run = self._run_repository.save(run)
        logger.info("Created run %s", run)
        return JSONResponse(content=self._object_mapper.to_dict(run), status_code=201)

    def status(self, run_id: int):
        status_by_run_id = (
            self._test_result_repository.find_execution_status_by_run_ids({run_id})
        )

        if not status_by_run_id.get(run_id):
            return Response(status_code=404)

        return JSONResponse(
            content={
                "status": RunStatusCalculator()
                .calculate(status_by_run_id.get(run_id))
                .name
            }
        )

    async def create_full_run(self, request: Request):
        request_json = await request.json()
        errors = CreateFullRunValidator(self._project_repository).validate(request_json)
        if errors:
            return JSONResponse(content=errors, status_code=BAD_REQUEST)

        create_full_run_dto = self._object_mapper.from_dict(
            request_json, CreateFullRunDto
        )

        run = self._create_full_run_usecase.create_full_run(create_full_run_dto)
        return JSONResponse(content=self._object_mapper.to_dict(run), status_code=201)

    def run_events_for_project(self, project_id):
        if not self._project_repository.find_by_id(project_id):
            return Response(status_code=404)
        message_queue = self._message_queue.component

        response = flask.Response(
            format_sse(
                message_queue.get_event_stream(
                    "run_events", str(project_id), self._object_mapper
                )
            ),
            mimetype="text/event-stream",
        )
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    def summary(self, run_id):
        run = self._run_repository.find_by_id(run_id)
        if not run:
            return Response(status_code=404)
        status_by_run_id = (
            self._test_result_repository.find_execution_status_by_project_id(
                run.project_id
            )
        )
        status = self._run_status_calculator.calculate(
            status_by_run_id.get(run.id, set())
        )
        run_dto = RunDto(
            id=run.id,
            project_id=run.id,
            started_at=run.started_at.isoformat(),
            status=RunStatusDto(status),
        )
        suite_count = self._suite_result_repository.suite_count_by_run_id(run_id)
        test_count = self._test_result_repository.test_count_by_run_id(run_id)
        failed_test_count = self._test_result_repository.failed_test_count_by_run_id(
            run_id
        )
        duration = self._test_result_repository.duration_by_run_id(run_id)
        run_summary_dto = RunSummaryDto(
            run=run_dto,
            suite_count=suite_count,
            test_count=test_count,
            failed_test_count=failed_test_count,
            duration=duration,
        )
        return JSONResponse(content=self._object_mapper.to_dict(run_summary_dto))
