import schedule
import sentry_sdk

import cato_server.server_logging
from cato_server.utils.background_task_creator import BackgroundTaskCreator

logger = cato_server.server_logging.logger

from cato_server.startup import (
    parse_config_from_cli,
    setup_logger,
    create_bindings,
    create_obj_graph,
)
from cato_server.utils.background_scheduler_runner import BackgroundSchedulerRunner


def main():
    config = parse_config_from_cli()
    setup_logger(config, "log_cato_beat.txt")
    bindings = create_bindings(config)
    obj_graph = create_obj_graph(bindings)

    if config.sentry_configuration.url:
        logger.info(
            "Initializing sentry sdk with url %s", config.sentry_configuration.url
        )
        sentry_sdk.init(
            config.sentry_configuration.url,
            traces_sample_rate=1.0,
            release=cato_server.__version__,
        )

    task_creator = obj_graph.provide(BackgroundTaskCreator)
    task_creator.create()
    scheduler_runner = BackgroundSchedulerRunner(schedule)  # type: ignore
    scheduler_runner.start_scheduler_loop()


if __name__ == "__main__":
    main()
