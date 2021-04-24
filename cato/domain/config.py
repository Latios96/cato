from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict

from cato.domain.test_suite import TestSuite


@dataclass
class Config:
    project_name: str
    test_suites: List[TestSuite]
    variables: Dict[str, str] = field(default_factory=dict)

    def for_json(self):
        return {
            "project_name": self.project_name,
            "suites": self.test_suites,
            "variables": self.variables,
        }

    @property
    def suite_count(self):
        return len(self.test_suites)

    @property
    def test_count(self):
        return sum(map(lambda x: len(x.tests), self.test_suites))


@dataclass
class RunConfig:
    project_name: str
    resource_path: str
    test_suites: List[TestSuite]
    output_folder: str
    variables: Dict[str, str] = field(default_factory=dict)

    def for_json(self):
        return {
            "project_name": self.project_name,
            "suites": self.test_suites,
            "variables": self.variables,
        }

    @property
    def suite_count(self):
        return len(self.test_suites)

    @property
    def test_count(self):
        return sum(map(lambda x: len(x.tests), self.test_suites))

    @classmethod
    def from_config(
        cls, config: Config, resource_path: str, output_folder: str
    ) -> RunConfig:
        return RunConfig(
            project_name=config.project_name,
            resource_path=resource_path,
            test_suites=config.test_suites,
            output_folder=output_folder,
            variables=config.variables,
        )

    def to_config(self) -> Config:
        return Config(self.project_name, self.test_suites, self.variables)
