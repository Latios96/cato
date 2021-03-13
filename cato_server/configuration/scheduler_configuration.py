from dataclasses import dataclass


@dataclass
class SchedulerConfiguration:
    name = "None"


@dataclass
class DeadlineSchedulerConfiguration(SchedulerConfiguration):
    name = "Deadline"
    url: str
