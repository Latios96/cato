import datetime
from dataclasses import dataclass


@dataclass
class SessionConfiguration:
    lifetime: datetime.timedelta
