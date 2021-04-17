from dataclasses import dataclass

from cato.domain.config import Config


@dataclass
class SubmissionInfo:
    id: int
    config: Config
    run_id: int
    resource_path: str
    executable: str
