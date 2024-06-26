from dataclasses import dataclass, field
from typing import List, Dict

from cato_common.domain.test_suite import TestSuite


@dataclass
class Config:
    project_name: str
    suites: List[TestSuite]
    variables: Dict[str, str] = field(default_factory=dict)

    @property
    def suite_count(self):
        return len(self.suites)

    @property
    def test_count(self):
        return sum(map(lambda x: len(x.tests), self.suites))


@dataclass
class RunConfig:
    project_name: str
    resource_path: str
    suites: List[TestSuite]
    output_folder: str
    variables: Dict[str, str] = field(default_factory=dict)

    @property
    def suite_count(self):
        return len(self.suites)

    @property
    def test_count(self):
        return sum(map(lambda x: len(x.tests), self.suites))

    @classmethod
    def from_config(cls, config, resource_path, output_folder):
        # type: (Config, str, str)->RunConfig
        return RunConfig(
            project_name=config.project_name,
            resource_path=resource_path,
            suites=config.suites,
            output_folder=output_folder,
            variables=config.variables,
        )

    def to_config(self) -> Config:
        return Config(self.project_name, self.suites, self.variables)
