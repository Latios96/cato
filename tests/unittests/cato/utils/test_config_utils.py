import json
import os

import pytest

from cato.utils.config_utils import (
    resolve_config_path,
    read_url_from_config_path,
    UrlMissingException,
)


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


class TestReadUrlFromConfigPath:
    def test_should_read_url_from_config(self, tmp_path):
        config_path = tmp_path / "cato.json"
        with open(config_path, "w") as f:
            json.dump({"serverUrl": "theUrl"}, f)

        url = read_url_from_config_path(str(config_path), require_url=True)

        assert url == "theUrl"

    def test_should_throw_if_no_url_in_config_and_require_url_is_true(self, tmp_path):
        config_path = tmp_path / "cato.json"
        with open(config_path, "w") as f:
            json.dump({}, f)

        with pytest.raises(UrlMissingException):
            read_url_from_config_path(str(config_path), require_url=True)

    def test_should_not_throw_if_no_url_in_config_and_require_url_is_false(
        self, tmp_path
    ):
        config_path = tmp_path / "cato.json"
        with open(config_path, "w") as f:
            json.dump({}, f)

        url = read_url_from_config_path(str(config_path), require_url=False)

        assert url == "<not given>"
