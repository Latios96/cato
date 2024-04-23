from dataclasses import dataclass


@dataclass
class PerformanceTrace:
    id: int
    performance_trace_json: str
