import dataclasses

import flask
import pinject
from flask import jsonify, send_file

from cato.domain.test_identifier import TestIdentifier
from cato.storage.sqlalchemy.sqlalchemy_config import SqlAlchemyConfig
from cato.storage.sqlalchemy.sqlalchemy_deduplicating_file_storage import (
    SqlAlchemyDeduplicatingFileStorage,
)
from cato.storage.sqlalchemy.sqlalchemy_project_repository import (
    SqlAlchemyProjectRepository,
)
from cato.storage.sqlalchemy.sqlalchemy_run_repository import SqlAlchemyRunRepository
from cato.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
)
from cato.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)

app = flask.Flask(__name__)
app.config["DEBUG"] = True

config = SqlAlchemyConfig()


class TestExecutionReporterBindings(pinject.BindingSpec):
    def configure(self, bind):
        bind("project_repository", to_class=SqlAlchemyProjectRepository)
        bind("run_repository", to_class=SqlAlchemyRunRepository)
        bind("suite_result_repository", to_class=SqlAlchemySuiteResultRepository)
        bind("test_result_repository", to_class=SqlAlchemyTestResultRepository)
        bind("file_storage", to_class=SqlAlchemyDeduplicatingFileStorage)
        bind("root_path", to_instance=config.get_file_storage_path())
        bind("session_maker", to_instance=config.get_session_maker())


obj_graph = pinject.new_object_graph(binding_specs=[TestExecutionReporterBindings()])


@app.route("/api/v1/projects", methods=["GET"])
def all_projects():
    project_repo: SqlAlchemyProjectRepository = obj_graph.provide(
        SqlAlchemyProjectRepository
    )
    all_projects = project_repo.find_all()
    return jsonify(all_projects)


@app.route("/api/v1/runs/project/<project_id>", methods=["GET"])
def run_by_project(project_id):
    run_repo: SqlAlchemyRunRepository = obj_graph.provide(SqlAlchemyRunRepository)
    runs = run_repo.find_by_project_id(project_id)
    return jsonify(runs)


@app.route("/api/v1/suite_results/run/<run_id>", methods=["GET"])
def suite_result_by_run(run_id):
    suite_result_repo: SqlAlchemySuiteResultRepository = obj_graph.provide(
        SqlAlchemySuiteResultRepository
    )
    suite_results = suite_result_repo.find_by_run_id(run_id)
    return jsonify(suite_results)


@app.route(
    "/api/v1/test_results/suite_result/<int:suite_result_id>/<string:suite_name>/<string:test_name>",
    methods=["GET"],
)
def get_test_result_by_suite_and_identifier(suite_result_id, suite_name, test_name):
    suite_result_repo: SqlAlchemyTestResultRepository = obj_graph.provide(
        SqlAlchemyTestResultRepository
    )
    suite_result = suite_result_repo.find_by_suite_result_and_test_identifier(
        suite_result_id, TestIdentifier(suite_name, test_name)
    )
    if suite_result:
        suite_result = dataclasses.asdict(suite_result)
        suite_result.pop("output")
    return jsonify(suite_result)


@app.route("/api/v1/test_results/<int:test_result_id>/output", methods=["GET"])
def get_test_result_output(test_result_id):
    suite_result_repo: SqlAlchemyTestResultRepository = obj_graph.provide(
        SqlAlchemyTestResultRepository
    )
    suite_result = suite_result_repo.find_by_id(test_result_id)
    return jsonify(suite_result.output)


@app.route("/api/v1/files/<int:file_id>", methods=["GET"])
def get_file(file_id):
    file_storage: SqlAlchemyDeduplicatingFileStorage = obj_graph.provide(
        SqlAlchemyDeduplicatingFileStorage
    )
    file = file_storage.find_by_id(file_id)
    if file:
        return send_file(file_storage.get_path(file),attachment_filename=file.name)


if __name__ == "__main__":
    app.run()
