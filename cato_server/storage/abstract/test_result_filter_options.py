from dataclasses import dataclass
from typing import Optional

from cato_common.domain.test_failure_reason import TestFailureReason
from cato_server.storage.abstract.status_filter import StatusFilter


@dataclass
class TestResultFilterOptions:
    status: StatusFilter
    failure_reason: Optional[TestFailureReason]
