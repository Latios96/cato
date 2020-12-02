import argparse
import dataclasses
import os

import flask
import pinject
from flask import jsonify, send_file
from gevent.pywsgi import WSGIServer

import cato
import cato_server
from cato.domain.test_identifier import TestIdentifier
from cato.storage.sqlalchemy.sqlalchemy_deduplicating_file_storage import (
    SqlAlchemyDeduplicatingFileStorage,
)
from cato.storage.sqlalchemy.sqlalchemy_run_repository import SqlAlchemyRunRepository
from cato.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
)
from cato.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)
from cato_server.api.project_blueprint import ProjectsBlueprint
from cato_server.configuration.app_configuration_reader import AppConfigurationReader
from cato_server.configuration.bindings_factory import BindingsFactory, PinjectBindings


def create_app(bindings: PinjectBindings):
    obj_graph = pinject.new_object_graph(
        modules=[cato, cato_server], binding_specs=[bindings]
    )

    app = flask.Flask(__name__, static_url_path="/")
    app.config["DEBUG"] = True

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

    @app.route("/api/v1/test_results/suite_result/<int:suite_id>", methods=["GET"])
    def get_test_result_by_suite_id(suite_id):
        test_result_repo: SqlAlchemyTestResultRepository = obj_graph.provide(
            SqlAlchemyTestResultRepository
        )
        test_results = test_result_repo.find_by_suite_result(suite_id)
        mapped_results = []
        for result in test_results:
            result = dataclasses.asdict(result)
            result.pop("output")
            mapped_results.append(result)
        return jsonify(mapped_results)

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
        file_path = file_storage.get_path(file)
        if file and os.path.exists(file_path):
            return send_file(file_path, attachment_filename=file.name)

    @app.route("/", defaults={"path": ""})
    @app.route("/<string:path>")
    @app.route("/<path:path>")
    def index(path):
        print(path)
        return app.send_static_file("index.html")

    app.register_blueprint(obj_graph.provide(ProjectsBlueprint))

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--config',
                        help='path to config.ini')
    args = parser.parse_args()
    path = 'config.ini'
    if args.config:
        path = args.config

    config = AppConfigurationReader().read_file(path)
    bindings_factory: BindingsFactory = BindingsFactory(config)
    bindings = bindings_factory.create_bindings()
    app = create_app(bindings)
    http_server = WSGIServer(("localhost", config.port), app)
    print(f"Running on http://localhost:{config.port}")
    http_server.serve_forever()
