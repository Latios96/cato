import json
from io import StringIO

import pytest
from jsonschema import ValidationError

from cato.config.config_file_parser import JsonConfigParser
from cato.domain.test import Test
from cato.domain.test_suite import TestSuite

VALID_CONFIG = {
  "suites": [{
    "name": "My First Test Suite",
    "tests": [
      {
        "name": "My First Test",
        "command": "mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}"
      }
    ]
  }]
}

INVALID_CONFIG = {
  "suite": {
    "name": "My First Test Suite",
    "tests": [
      {
        "name": "My First Test",
        "cmd": "mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}"
      }
    ]
  }
}

def test_success():
    json_config_parser = JsonConfigParser()

    suites = json_config_parser.parse(StringIO(json.dumps(VALID_CONFIG)))

    assert suites == [
      TestSuite(name="My First Test Suite", tests=[
        Test(name="My First Test", command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}")
      ])
    ]


def test_failure():
  json_config_parser = JsonConfigParser()

  with pytest.raises(ValidationError):
    json_config_parser.parse(StringIO(json.dumps(INVALID_CONFIG)))