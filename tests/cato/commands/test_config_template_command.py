import os

from cato.commands.config_template_command import ConfigTemplateCommand
from cato.config.config_template_generator import ConfigTemplateGenerator


def test_should_write_config_template(tmp_path):
    template_command = ConfigTemplateCommand(ConfigTemplateGenerator())

    template_command.create_template(str(tmp_path))

    assert os.path.exists(os.path.join(str(tmp_path), "cato.json"))


def test_should_overwrite_config_template(tmp_path):
    template_command = ConfigTemplateCommand(ConfigTemplateGenerator())

    template_command.create_template(str(tmp_path))
    template_command.create_template(str(tmp_path))

    assert os.path.exists(os.path.join(str(tmp_path), "cato.json"))
