import os

from cato.commands.base_command import BaseCliCommand


def test_config_path_should_use_cwd():
    base_command = BaseCliCommand()

    path = base_command.config_path(None)

    assert path == os.path.join(os.getcwd(), "cato.json")


def test_config_path_should_use_provided_file():
    base_command = BaseCliCommand()

    path = base_command.config_path(os.path.join("my_folder", "catoo.json"))

    assert path == os.path.abspath(os.path.join("my_folder", "catoo.json"))


def test_config_path_should_use_provided_folder(tmp_path):
    base_command = BaseCliCommand()

    path = base_command.config_path(str(tmp_path))

    assert path == os.path.abspath(os.path.join(str(tmp_path), "cato.json"))
