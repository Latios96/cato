from dataclasses import dataclass
from cato.domain.config import Config
import logging

logger = logging.getLogger(__name__)


@dataclass
class SubmissionInfo:
    config: Config
    run_id: int
    resource_path: str
    executable: str


class AbstractSchedulerSubmitter:
    def submit_tests(self, submission_info: SubmissionInfo):
        raise NotImplementedError()
