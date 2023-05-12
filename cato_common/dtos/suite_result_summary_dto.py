from dataclasses import dataclass
from typing import Dict, List

from cato_common.dtos.test_result_short_summary_dto import TestResultShortSummaryDto
from cato_server.domain.run_status import RunStatus


@dataclass
class SuiteResultSummaryDto:
    id: int
    run_id: int
    suite_name: str
    suite_variables: Dict[str, str]
    status: RunStatus
    tests: List[TestResultShortSummaryDto]
