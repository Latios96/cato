import argparse
import dataclasses

import flask
import pinject
from flask import jsonify
from gevent.pywsgi import WSGIServer

import cato
import cato_server
from cato.domain.test_identifier import TestIdentifier
from cato.storage.sqlalchemy.sqlalchemy_run_repository import SqlAlchemyRunRepository
from cato.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
)
from cato.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)
from cato_server.api.files_blueprint import FilesBlueprint
from cato_server.api.projects_blueprint import ProjectsBlueprint
from cato_server.api.test_result_blueprint import TestResultsBlueprint
from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.app_configuration_reader import AppConfigurationReader
from cato_server.configuration.bindings_factory import BindingsFactory, PinjectBindings
from cato_server.server_logging import logger


def create_app(app_configuration: AppConfiguration, bindings: PinjectBindings):
    logger.info("Creating Flask app..")
    obj_graph = pinject.new_object_graph(
        modules=[cato, cato_server], binding_specs=[bindings]
    )

    app = flask.Flask(__name__, static_url_path="/")

    if app_configuration.debug == True:
        logger.info("Configuring app to run in debug mode")
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

    @app.route("/", defaults={"path": ""})
    @app.route("/<string:path>")
    @app.route("/<path:path>")
    def index(path):
        return app.send_static_file("index.html")

    app.register_blueprint(obj_graph.provide(ProjectsBlueprint), url_prefix="/api/v1")
    app.register_blueprint(obj_graph.provide(FilesBlueprint), url_prefix="/api/v1")
    app.register_blueprint(
        obj_graph.provide(TestResultsBlueprint), url_prefix="/api/v1"
    )

    return app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="path to config.ini")
    args = parser.parse_args()

    path = get_config_path(args)
    config = AppConfigurationReader().read_file(path)

    bindings_factory: BindingsFactory = BindingsFactory(config)
    bindings = bindings_factory.create_bindings()

    app = create_app(config, bindings)
    print(app.url_map)

    http_server = WSGIServer(("127.0.0.1", config.port), app)
    logger.info(f"Up and running on http://127.0.0.1:{config.port}")
    http_server.serve_forever()


def get_config_path(args):
    path = "config.ini"
    if args.config:
        path = args.config
    return path


if __name__ == "__main__":
    main()
