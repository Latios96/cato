from dataclasses import dataclass
from typing import Dict

from cato_server.domain.run_status import RunStatus


@dataclass
class SuiteResultDto:
    id: int
    run_id: int
    suite_name: str
    suite_variables: Dict[str, str]
    status: RunStatus
