from cato.commands.base_command import BaseCliCommand
from cato.config.config_template_generator import ConfigTemplateGenerator

import logging

logger = logging.getLogger(__name__)


class ConfigTemplateCommand(BaseCliCommand):
    def __init__(self, config_template_generator: ConfigTemplateGenerator):
        self._config_template_generator = config_template_generator

    def create_template(
        self,
        path: str,
    ):
        path = self._config_path(path)

        with open(path, "w") as f:
            self._config_template_generator.write(f)

        logger.info("Wrote config file to %s", path)
