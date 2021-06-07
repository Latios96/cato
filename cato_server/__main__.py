import argparse
import os.path
import signal

import pinject
import schedule
import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

import cato_server
import cato_server.server_logging
from cato_common.utils.bindings import imported_modules
from cato_server.api.about_blueprint import AboutBlueprint
from cato_server.api.files_blueprint import FilesBlueprint
from cato_server.api.images_blueprint import ImagesBlueprint
from cato_server.api.projects_blueprint import ProjectsBlueprint
from cato_server.api.runs_blueprint import RunsBlueprint
from cato_server.api.schedulers_blueprint import SchedulersBlueprint
from cato_server.api.submission_infos_blueprint import SubmissionInfosBlueprint
from cato_server.api.suite_results_blueprint import SuiteResultsBlueprint
from cato_server.api.test_heartbeat_blueprint import TestHeartbeatBlueprint
from cato_server.api.test_result_blueprint import TestResultsBlueprint
from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.app_configuration_reader import AppConfigurationReader
from cato_server.configuration.bindings_factory import BindingsFactory, PinjectBindings
from cato_server.utils.background_scheduler_runner import BackgroundSchedulerRunner
from cato_server.utils.background_task_creator import BackgroundTaskCreator

logger = cato_server.server_logging.logger

BANNER = r"""

 ,-----.            ,--.              ,---.                                              
'  .--./  ,--,--. ,-'  '-.  ,---.    '   .-'   ,---.  ,--.--. ,--.  ,--.  ,---.  ,--.--. 
|  |     ' ,-.  | '-.  .-' | .-. |   `.  `-.  | .-. : |  .--'  \  `'  /  | .-. : |  .--' 
'  '--'\ \ '-'  |   |  |   ' '-' '   .-'    | \   --. |  |      \    /   \   --. |  |    
 `-----'  `--`--'   `--'    `---'    `-----'   `----' `--'       `--'     `----' `--'    
"""


def create_app(
    app_configuration: AppConfiguration,
    bindings: PinjectBindings,
    create_background_tasks=False,
):
    logger.info(BANNER)
    logger.info("Cato Server Version %s", cato_server.__version__)
    logger.info("Creating Flask app..")
    obj_graph = pinject.new_object_graph(
        modules=[*imported_modules(["cato", "cato_server"])], binding_specs=[bindings]
    )

    app = FastAPI()

    app.include_router(obj_graph.provide(AboutBlueprint), prefix="/api/v1")
    app.include_router(obj_graph.provide(ProjectsBlueprint), prefix="/api/v1")
    app.include_router(obj_graph.provide(FilesBlueprint), prefix="/api/v1")
    app.include_router(obj_graph.provide(ImagesBlueprint), prefix="/api/v1")
    app.include_router(obj_graph.provide(RunsBlueprint), prefix="/api/v1")
    app.include_router(obj_graph.provide(SchedulersBlueprint), prefix="/api/v1")
    app.include_router(obj_graph.provide(SubmissionInfosBlueprint), prefix="/api/v1")
    app.include_router(obj_graph.provide(SuiteResultsBlueprint), prefix="/api/v1")
    app.include_router(obj_graph.provide(TestHeartbeatBlueprint), prefix="/api/v1")
    app.include_router(obj_graph.provide(TestResultsBlueprint), prefix="/api/v1")

    static_directory = os.path.join(os.path.dirname(__file__), "static")
    if not os.path.exists(static_directory):
        os.makedirs(static_directory)
    app.mount("/", StaticFiles(directory=static_directory, html=True), name="static")

    if create_background_tasks:
        logger.info("Created background tasks..")
        task_creator = obj_graph.provide(BackgroundTaskCreator)
        task_creator.create()
        app.scheduler_runner = BackgroundSchedulerRunner(schedule)
        app.scheduler_runner.start()

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

    app = create_app(config, bindings, create_background_tasks=True)

    signal.signal(
        signal.SIGINT,
        lambda x, y: (app.scheduler_runner.stop(), exit(0)),
    )

    logger.info(f"Starting on http://127.0.0.1:{config.port}")
    uvicorn.run(app, host="127.0.0.1", port=config.port)


def get_config_path(args):
    path = "config.ini"
    if args.config:
        path = args.config
    return path


if __name__ == "__main__":
    main()
