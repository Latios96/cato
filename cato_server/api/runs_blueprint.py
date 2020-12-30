import logging
from http.client import BAD_REQUEST

import flask
from dateutil.parser import parse
from flask import Blueprint, jsonify, request, abort

from cato_api_models.catoapimodels import (
    RunDto,
    RunStatusDto,
    RunSummaryDto,
    CreateFullRunDto,
)
from cato_server.api.base_blueprint import BaseBlueprint
from cato_server.api.utils import format_sse
from cato_server.api.validators.run_validators import (
    CreateRunValidator,
    CreateFullRunValidator,
)
from cato_server.configuration.optional_component import OptionalComponent
from cato_server.domain.run import Run
from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.queues.abstract_message_queue import AbstractMessageQueue
from cato_server.run_status_calculator import RunStatusCalculator
from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)
from cato_server.usecases.create_full_run import CreateFullRunUsecase

logger = logging.getLogger(__name__)


class RunsBlueprint(BaseBlueprint):
    def __init__(
        self,
        run_repository: RunRepository,
        project_repository: ProjectRepository,
        test_result_repository: TestResultRepository,
        create_full_run_usecase: CreateFullRunUsecase,
        message_queue: OptionalComponent[AbstractMessageQueue],
        suite_result_repository: SuiteResultRepository,
        object_mapper: ObjectMapper,
    ):
        super(RunsBlueprint, self).__init__("runs", __name__)
        self._run_repository = run_repository
        self._project_repository = project_repository
        self._test_result_repository = test_result_repository
        self._create_full_run_usecase = create_full_run_usecase
        self._message_queue = message_queue
        self._suite_result_repository = suite_result_repository
        self._object_mapper = object_mapper

        self._run_status_calculator = RunStatusCalculator()

        self.route("/runs/project/<project_id>", methods=["GET"])(self.run_by_project)
        self.route("/runs", methods=["POST"])(self.create_run)
        self.route("/runs/full", methods=["POST"])(self.create_full_run)
        self.route("/runs/<int:run_id>/status", methods=["GET"])(self.status)
        self.route("/runs/<int:run_id>/summary", methods=["GET"])(self.summary)

        if self._message_queue.is_available():
            logger.info("Message queue is available, adding run events route")
            self.route("/runs/events/<int:project_id>", methods=["GET"])(
                self.run_events_for_project
            )

    def run_by_project(self, project_id):
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
        return self.json_response(self._object_mapper.many_to_json(run_dtos))

    def create_run(self):
        request_json = request.get_json()
        errors = CreateRunValidator(self._project_repository).validate(request_json)
        if errors:
            return jsonify(errors), BAD_REQUEST

        run = Run(
            id=0,
            project_id=request_json["project_id"],
            started_at=parse(request_json["started_at"]),
        )
        run = self._run_repository.save(run)
        logger.info("Created run %s", run)
        return self.json_response(self._object_mapper.to_json(run)), 201

    def status(self, run_id):
        status_by_run_id = (
            self._test_result_repository.find_execution_status_by_run_ids({run_id})
        )

        if not status_by_run_id.get(run_id):
            abort(404)

        return {
            "status": RunStatusCalculator().calculate(status_by_run_id.get(run_id)).name
        }

    def create_full_run(self):
        request_json = request.get_json()
        errors = CreateFullRunValidator(self._project_repository).validate(request_json)
        if errors:
            return jsonify(errors), BAD_REQUEST

        create_full_run_dto = self._object_mapper.from_dict(
            request_json, CreateFullRunDto
        )

        run = self._create_full_run_usecase.create_full_run(create_full_run_dto)
        return self.json_response(self._object_mapper.to_json(run)), 201

    def run_events_for_project(self, project_id):
        if not self._project_repository.find_by_id(project_id):
            abort(404)
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
            abort(404)
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
        return self.json_response(self._object_mapper.to_json(run_summary_dto))
