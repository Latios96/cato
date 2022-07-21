import sentry_sdk

import cato_server.server_logging
from cato_server.task_queue.cato_celery import CatoCelery

logger = cato_server.server_logging.logger

from cato_server.startup import (
    parse_config_from_cli,
    setup_logger,
    create_bindings,
    create_obj_graph,
)


def main():
    config = parse_config_from_cli()
    setup_logger(config, "log_cato_worker.txt")
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

    celery_app = obj_graph.provide(CatoCelery)

    argv = ["worker", "--loglevel=INFO", "--concurrency=1", "--pool=solo"]
    celery_app.app.worker_main(argv)


if __name__ == "__main__":
    main()
