import datetime
import logging
from http.client import BAD_REQUEST

from dateutil.parser import parse
from flask import Blueprint, jsonify, request, abort

from cato_server.domain.machine_info import MachineInfo
from cato_server.domain.run import Run
from cato_server.domain.suite_result import SuiteResult
from cato_server.domain.test_identifier import TestIdentifier
from cato_server.domain.test_result import TestResult
from cato_server.mappers.create_full_run_dto_class_mapper import (
    CreateFullRunDtoClassMapper,
)
from cato_server.mappers.execution_status_value_mapper import ExecutionStatusValueMapper
from cato_server.mappers.run_class_mapper import RunClassMapper
from cato_server.run_status_calculator import RunStatusCalculator
from cato_server.api.validators.run_validators import (
    CreateRunValidator,
    CreateFullRunValidator,
)
from cato_server.storage.abstract.abstract_test_result_repository import (
    TestResultRepository,
)
from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository

logger = logging.getLogger(__name__)


class RunsBlueprint(Blueprint):
    def __init__(
        self,
        run_repository: RunRepository,
        project_repository: ProjectRepository,
        test_result_repository: TestResultRepository,
        suite_result_repository: SuiteResultRepository,
    ):
        super(RunsBlueprint, self).__init__("runs", __name__)
        self._run_repository = run_repository
        self._project_repository = project_repository
        self._test_result_repository = test_result_repository
        self._suite_result_repository = suite_result_repository

        self.route("/runs/project/<project_id>", methods=["GET"])(self.run_by_project)
        self.route("/runs", methods=["POST"])(self.create_run)
        self.route("/runs/full", methods=["POST"])(self.create_full_run)
        self.route("/runs/<int:run_id>/status", methods=["GET"])(self.status)

    def run_by_project(self, project_id):
        runs = self._run_repository.find_by_project_id(project_id)
        return jsonify(runs)

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
        return jsonify(run), 201

    def status(self, run_id):
        test_results = self._test_result_repository.find_by_run_id(run_id)

        if not test_results:
            abort(404)

        return {"status": RunStatusCalculator().calculate(test_results).name}

    def create_full_run(self):
        request_json = request.get_json()
        errors = CreateFullRunValidator(self._project_repository).validate(request_json)
        if errors:
            return jsonify(errors), BAD_REQUEST

        create_full_run_dto = CreateFullRunDtoClassMapper().map_from_dict(request_json)

        run = Run(
            id=0,
            project_id=create_full_run_dto.project_id,
            started_at=datetime.datetime.now(),
        )
        run = self._run_repository.save(run)
        logger.info("Created run %s", run)

        for suite_dto in create_full_run_dto.test_suites:
            suite_result = SuiteResult(
                id=0,
                run_id=run.id,
                suite_name=suite_dto.suite_name,
                suite_variables=suite_dto.suite_variables,
            )
            suite_result = self._suite_result_repository.save(suite_result)
            logger.info("Created suite %s", suite_result)
            tests = []
            for test_dto in suite_dto.tests:
                tests.append(
                    TestResult(
                        id=0,
                        suite_result_id=suite_result.id,
                        test_name=test_dto.test_name,
                        test_identifier=TestIdentifier.from_string(
                            test_dto.test_identifier
                        ),
                        test_command=test_dto.test_command,
                        test_variables=test_dto.test_variables,
                        machine_info=MachineInfo(
                            cpu_name=test_dto.machine_info.cpu_name,
                            cores=test_dto.machine_info.cores,
                            memory=test_dto.machine_info.memory,
                        ),
                        execution_status=ExecutionStatusValueMapper().map_from(
                            test_dto.execution_status.value
                        ),
                    )
                )
            saved_tests = self._test_result_repository.insert_many(tests)
            logger.info(
                "Created %s test results for suite %s",
                len(saved_tests),
                suite_result.suite_name,
            )
        return jsonify(RunClassMapper().map_to_dict(run)), 201
