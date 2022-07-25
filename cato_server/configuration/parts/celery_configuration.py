from dataclasses import dataclass


@dataclass
class CeleryConfiguration:
    broker_url: str
