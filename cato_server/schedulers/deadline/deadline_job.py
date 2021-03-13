from dataclasses import dataclass
from typing import Dict


@dataclass
class DeadlineJob:
    job_info: Dict[str, str]
    plugin_info: Dict[str, str]
