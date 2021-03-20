import os

import pytest


@pytest.fixture
def scenario_context():
    return {}


@pytest.fixture
def dir_changer():
    old_dir = os.getcwd()
    yield
    os.chdir(old_dir)
