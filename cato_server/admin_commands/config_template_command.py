import os

from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)

import logging

from cato_server.configuration.app_configuration_writer import AppConfigurationWriter

logger = logging.getLogger(__name__)


class ConfigTemplateCommand:
    def create_config_template(self, path: str, try_out: bool) -> None:
        if not try_out:
            config = AppConfigurationDefaults().create()
        else:
            config_folder = os.path.dirname(path)
            config_folder = os.path.abspath(config_folder)
            config = AppConfigurationDefaults().create_ready_to_use(
                config_folder=config_folder
            )

        logger.info("Write config to %s", path)
        AppConfigurationWriter().write_file(config, path)
