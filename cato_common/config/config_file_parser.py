import json
import os
from typing import IO, List, Dict

from jsonschema import validate

from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.config import Config
from cato_common.domain.test import Test
from cato_common.domain.test_suite import TestSuite
from cato_common.utils.typing import safe_cast


class JsonConfigParser:
    def parse(self, path: str, stream: IO = None) -> Config:
        if not stream:
            stream = open(path)
        data = self._read_json_from_stream(stream)

        return self.parse_dict(data)

    def parse_dict(self, data: Dict) -> Config:
        schema = self._read_json_from_file(self._schema_path())
        validate(instance=data, schema=schema)
        return Config(
            data["projectName"],
            self._transform_suites(data),
            variables=data["variables"] if data.get("variables") else {},
        )

    def _read_json_from_file(self, path: str) -> dict:
        with open(path) as f:
            return safe_cast(dict, json.load(f))

    def _read_json_from_stream(self, stream: IO) -> dict:
        return safe_cast(dict, json.load(stream))

    def _schema_path(self) -> str:
        return os.path.join(os.path.dirname(__file__), "schema.json")

    def _transform_suites(self, data: dict) -> List[TestSuite]:
        suites = []
        for suite in data["suites"]:
            name = suite["name"]
            tests = self._transform_test(suite)
            suites.append(
                TestSuite(
                    name=name,
                    tests=tests,
                    variables=suite["variables"] if suite.get("variables") else {},
                )
            )

        return suites

    def _transform_test(self, suite: Dict) -> List[Test]:
        tests = []
        for test in suite["tests"]:
            comparison_settings = self._read_comparison_settings(test)
            tests.append(
                Test(
                    name=test["name"],
                    command=test["command"],
                    variables=test["variables"] if test.get("variables") else {},
                    comparison_settings=comparison_settings,
                )
            )
        return tests

    def _read_comparison_settings(self, test):
        comparison_settings_dict = test.get("comparison_settings")
        if comparison_settings_dict:
            return ComparisonSettings(
                method=ComparisonMethod(comparison_settings_dict["method"]),
                threshold=comparison_settings_dict["threshold"],
            )
        return ComparisonSettings.default()
