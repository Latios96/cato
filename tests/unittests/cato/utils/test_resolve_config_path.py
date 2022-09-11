import os

from cato.utils.resolve_config_path import resolve_config_path


def test_config_path_should_use_cwd():
    path = resolve_config_path(None)

    assert path == os.path.join(os.getcwd(), "cato.json")


def test_config_path_should_use_provided_file():
    path = resolve_config_path(os.path.join("my_folder", "catoo.json"))

    assert path == os.path.abspath(os.path.join("my_folder", "catoo.json"))


def test_config_path_should_use_provided_folder(tmp_path):
    path = resolve_config_path(str(tmp_path))

    assert path == os.path.abspath(os.path.join(str(tmp_path), "cato.json"))
