from cato.commands.base_command import BaseCliCommand
from cato.config.config_template_generator import ConfigTemplateGenerator


class ConfigTemplateCommand(BaseCliCommand):
    def __init__(self, config_template_generator: ConfigTemplateGenerator):
        self._config_template_generator = config_template_generator

    def create_template(
        self,
        path: str,
    ):
        path = self.config_path(path)

        with open(path, "w") as f:
            self._config_template_generator.write(f)
