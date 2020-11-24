from dataclasses import dataclass
import datetime


@dataclass
class Run:
    id: int
    project_id: int
    started_at: datetime.datetime
