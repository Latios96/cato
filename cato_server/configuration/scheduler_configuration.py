from dataclasses import dataclass


@dataclass
class SchedulerConfiguration(object):
    name = "None"


@dataclass
class DeadlineSchedulerConfiguration(object):
    name = "Deadline"
    url: str
