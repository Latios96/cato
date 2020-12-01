from dataclasses import dataclass
from typing import Dict


@dataclass
class SuiteResult:
    id: int
    run_id: int
    suite_name: str
    suite_variables: Dict[str, str]
