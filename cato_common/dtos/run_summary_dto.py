from dataclasses import dataclass

from cato_common.dtos.run_dto import RunDto


@dataclass
class RunSummaryDto:
    run: RunDto
    suite_count: int
    test_count: int
    waiting_test_count: int
    running_test_count: int
    failed_test_count: int
    succeeded_test_count: int
