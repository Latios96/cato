import multiprocessing

import uvicorn

import cato_server.server_logging
from cato_server.startup import (
    parse_config_from_cli,
    setup_logger,
    create_bindings,
    create_app,
    setup_app_for_production,
)

logger = cato_server.server_logging.logger


config = parse_config_from_cli()
setup_logger(config)
bindings = create_bindings(config)
raw_app = create_app(config, bindings, create_background_tasks=config.debug)
app = setup_app_for_production(raw_app, config)
worker_count = config.workers if config.workers else multiprocessing.cpu_count()
workers = None if config.debug else worker_count


def main():
    logger.info(
        f"Starting on http://{config.hostname}:{config.port} with {workers} workers"
    )
    uvicorn.run(
        "cato_server.__main__:app",
        host=config.hostname,
        port=config.port,
        workers=workers,
    )


if __name__ == "__main__":
    main()
