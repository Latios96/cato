import dataclasses
import json
import time
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from typing import List

from cato_common.domain.test_identifier import TestIdentifier


class ChromiumTracingDurationEventType(str, Enum):
    BEGIN = "B"
    END = "E"


@dataclass(frozen=True)
class ChromiumTracingDurationEvent:
    name: str
    timestamp: float
    type: ChromiumTracingDurationEventType


class ImageType(str, Enum):
    OUTPUT = "OUTPUT"
    REFERENCE = "REFERENCE"
    DIFF = "DIFF"


class PerformanceStatsCollector:
    def __init__(self):
        self._events: List[ChromiumTracingDurationEvent] = []
        self._start_time = self._current_microseconds()

    @contextmanager
    def collect_cato_run_timing(self):
        with self._collect_event_timing("Cato Run"):
            yield

    @contextmanager
    def collect_create_run_timing(self):
        with self._collect_event_timing("Create run in DB"):
            yield

    @contextmanager
    def collect_suite_timing(self, suite_name):
        with self._collect_event_timing(
            f"Suite {suite_name}",
        ):
            yield

    @contextmanager
    def collect_test_timing(self, test_identifier: TestIdentifier):
        with self._collect_event_timing(
            f"Test {test_identifier}",
        ):
            yield

    @contextmanager
    def collect_test_command_execution_timing(self):
        with self._collect_event_timing("test command execution"):
            yield

    @contextmanager
    def collect_image_upload_timing(self, image_type: ImageType):
        with self._collect_event_timing(f"upload {image_type.name.lower()} image"):
            yield

    @contextmanager
    def collect_image_comparison_timing(self):
        with self._collect_event_timing(f"image comparison"):
            yield

    @contextmanager
    def collect_start_test_request_timing(self):
        with self._collect_event_timing(f"start test request"):
            yield

    @contextmanager
    def collect_report_test_result(self):
        with self._collect_event_timing(f"report test result"):
            yield

    @contextmanager
    def collect_finish_test_timing(self):
        with self._collect_event_timing(f"finish test"):
            yield

    @contextmanager
    def collect_upload_log_output_timing(self):
        with self._collect_event_timing(f"upload log output"):
            yield

    def get_json_trace(self):
        chrome_trace_events = []
        for event in self._events:
            chrome_trace_events.append(
                {
                    "name": event.name,
                    "ph": event.type.value,
                    "pid": 0,
                    "tid": 0,
                    "ts": event.timestamp,
                }
            )
        json_data = {"traceEvents": chrome_trace_events}

        return json.dumps(json_data, separators=(",", ":"))

    def _current_microseconds(self):
        return time.time() * 1000000

    def _current_timestamp(self):
        return self._current_microseconds() - self._start_time

    def _produce_duration_start_event(self, name):
        return ChromiumTracingDurationEvent(
            name=name,
            timestamp=self._current_timestamp(),
            type=ChromiumTracingDurationEventType.BEGIN,
        )

    @contextmanager
    def _collect_event_timing(self, event_name):
        start_event = self._produce_duration_start_event(event_name)
        self._events.append(start_event)

        yield

        finish_event = dataclasses.replace(
            start_event,
            type=ChromiumTracingDurationEventType.END,
            timestamp=self._current_timestamp(),
        )
        self._events.append(finish_event)
