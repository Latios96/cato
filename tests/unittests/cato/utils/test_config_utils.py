import os

from cato.utils.config_utils import resolve_config_path


class TestResolveConfigPath:
    def test_config_path_should_use_cwd(self):
        path = resolve_config_path(None)

        assert path == os.path.join(os.getcwd(), "cato.json")

    def test_config_path_should_use_provided_file(self):
        path = resolve_config_path(os.path.join("my_folder", "catoo.json"))

        assert path == os.path.abspath(os.path.join("my_folder", "catoo.json"))

    def test_config_path_should_use_provided_folder(self, tmp_path):
        path = resolve_config_path(str(tmp_path))

        assert path == os.path.abspath(os.path.join(str(tmp_path), "cato.json"))
