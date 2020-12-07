import argparse
import datetime

import flask
import pinject
from flask.json import JSONEncoder
from gevent.pywsgi import WSGIServer
from werkzeug.exceptions import HTTPException

import cato
import cato_server
import cato_server.server_logging
from cato_server.api.about_blueprint import AboutBlueprint
from cato_server.api.files_blueprint import FilesBlueprint
from cato_server.api.projects_blueprint import ProjectsBlueprint
from cato_server.api.runs_blueprint import RunsBlueprint
from cato_server.api.suite_results_blueprint import SuiteResultsBlueprint
from cato_server.api.test_result_blueprint import TestResultsBlueprint
from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.app_configuration_reader import AppConfigurationReader
from cato_server.configuration.bindings_factory import BindingsFactory, PinjectBindings

logger = cato_server.server_logging.logger

BANNER = r"""

 ,-----.            ,--.              ,---.                                              
'  .--./  ,--,--. ,-'  '-.  ,---.    '   .-'   ,---.  ,--.--. ,--.  ,--.  ,---.  ,--.--. 
|  |     ' ,-.  | '-.  .-' | .-. |   `.  `-.  | .-. : |  .--'  \  `'  /  | .-. : |  .--' 
'  '--'\ \ '-'  |   |  |   ' '-' '   .-'    | \   --. |  |      \    /   \   --. |  |    
 `-----'  `--`--'   `--'    `---'    `-----'   `----' `--'       `--'     `----' `--'    
"""


def create_app(app_configuration: AppConfiguration, bindings: PinjectBindings):
    logger.info(BANNER)
    logger.info("Cato Server Version %s", cato_server.__version__)
    logger.info("Creating Flask app..")
    obj_graph = pinject.new_object_graph(
        modules=[cato, cato_server], binding_specs=[bindings]
    )

    app = flask.Flask(__name__, static_url_path="/")

    if app_configuration.debug is True:
        logger.info("Configuring app to run in debug mode")
        app.config["DEBUG"] = True

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
    app.register_blueprint(obj_graph.provide(RunsBlueprint), url_prefix="/api/v1")
    app.register_blueprint(
        obj_graph.provide(SuiteResultsBlueprint), url_prefix="/api/v1"
    )
    app.register_blueprint(obj_graph.provide(AboutBlueprint), url_prefix="/api/v1")

    @app.errorhandler(Exception)
    def handle_500(e):
        if isinstance(e, HTTPException):
            return e
        logger.error(e, exc_info=True)
        return "Internal Server Error", 500

    class CustomJSONEncoder(JSONEncoder):
        def default(self, obj):
            try:
                if isinstance(obj, datetime.datetime):
                    return obj.isoformat()
                iterable = iter(obj)
            except TypeError:
                pass
            else:
                return list(iterable)
            return JSONEncoder.default(self, obj)

    app.json_encoder = CustomJSONEncoder

    return app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", help="path to config.ini")
    args = parser.parse_args()

    path = get_config_path(args)
    config = AppConfigurationReader().read_file(path)

    if config.logging_configuration.use_file_handler:
        cato_server.server_logging.setup_file_handler(
            "log.txt",
            config.logging_configuration.max_bytes,
            config.logging_configuration.backup_count,
        )

    bindings_factory: BindingsFactory = BindingsFactory(config)
    bindings = bindings_factory.create_bindings()

    app = create_app(config, bindings)

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
