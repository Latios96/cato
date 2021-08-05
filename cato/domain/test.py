from dataclasses import dataclass
from typing import Dict

from cato.domain.comparison_settings import ComparisonSettings
from cato.domain.validation import validate_name


@dataclass
class Test:
    name: str
    command: str
    variables: Dict[str, str]
    comparison_settings: ComparisonSettings

    def __post_init__(self):
        validate_name(self.name)

    __test__ = False
