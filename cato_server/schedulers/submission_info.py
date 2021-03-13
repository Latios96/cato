from dataclasses import dataclass

from cato.domain.config import Config


@dataclass
class SubmissionInfo:
    config: Config
    run_id: int
    resource_path: str
    executable: str
