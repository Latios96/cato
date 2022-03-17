import datetime
from dataclasses import dataclass


@dataclass
class SessionConfiguration:
    lifetime: datetime.timedelta

    @staticmethod
    def default():
        return SessionConfiguration(lifetime=datetime.timedelta(hours=2))
