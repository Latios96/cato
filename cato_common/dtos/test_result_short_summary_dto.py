from dataclasses import dataclass
from typing import Optional

from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.unified_test_status import UnifiedTestStatus


@dataclass
class TestResultShortSummaryDto:
    __test__ = False
    id: int
    name: str
    test_identifier: TestIdentifier
    unified_test_status: UnifiedTestStatus
    thumbnail_file_id: Optional[int]
    seconds: Optional[float]
