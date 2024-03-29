import os
import shutil
import sys

import pytest


@pytest.fixture
def cato_config(tmp_path, test_resource_provider):
    config_folder = os.path.join(str(tmp_path), "config_folder")
    shutil.copytree(
        test_resource_provider.resource_by_name("cato_cmd_integ_tests"), config_folder
    )

    config_path = os.path.join(config_folder, "cato.json")

    with open(config_path) as f:
        content = f.read()

    executable = sys.executable
    executable = executable.replace("\\", "/")

    content = content.replace('"python_exe": "python"', f'"python_exe": "{executable}"')

    with open(config_path, "wb") as f:
        f.write(content.encode())
    return config_folder, config_path
