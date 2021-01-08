import json
import os

import pytest

from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_suite import TestSuite


class ConfigFixture:
    TEST = Test(
        name="My_first_test",
        command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
        variables={"frame": "7"},
    )
    TEST_SUITE = TestSuite(
        name="My_first_test_Suite",
        tests=[TEST],
        variables={"my_var": "from_suite"},
    )
    CONFIG = Config(
        project_name="EXAMPLE_PROJECT",
        path="test",
        test_suites=[TEST_SUITE],
        output_folder="output",
        variables={"my_var": "from_config"},
    )


@pytest.fixture
def config_fixture():
    return ConfigFixture


@pytest.fixture
def config_file_fixture(tmp_path, config_fixture):
    path = os.path.join(str(tmp_path), "cato.json")
    with open(path, "w") as f:
        f.write(json.dumps(config_fixture.CONFIG))
    return path
