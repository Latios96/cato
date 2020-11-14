import json
import os
from typing import IO, List

from jsonschema import validate

from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_suite import TestSuite


class JsonConfigParser:
    def parse(self, path, stream: IO = None) -> Config:
        if not stream:
            stream = open(path)
        schema = self._read_json_from_file(self._schema_path())
        data = self._read_json_from_stream(stream)

        validate(instance=data, schema=schema)

        return Config(
            os.path.dirname(path),
            self._transform_suites(data),
            output_folder=os.getcwd(),
        )

    def _read_json_from_file(self, path) -> dict:
        with open(path) as f:
            return json.load(f)

    def _read_json_from_stream(self, stream) -> dict:
        return json.load(stream)

    def _schema_path(self) -> str:
        return os.path.join(os.path.dirname(__file__), "schema.json")

    def _transform_suites(self, data: dict) -> List[TestSuite]:
        suites = []
        for suite in data["suites"]:
            name = suite["name"]
            tests = self._transform_test(suite)
            suites.append(TestSuite(name=name, tests=tests))

        return suites

    def _transform_test(self, suite) -> List[Test]:
        tests = []
        for test in suite["tests"]:
            tests.append(Test(name=test["name"], command=test["command"],variables={}))
        return tests
