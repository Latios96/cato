import dataclasses
import json
import time
from contextlib import contextmanager
from dataclasses import dataclass
from enum import Enum
from typing import List, Set, Iterator

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
        self._start_time: float = self._current_microseconds()

    @contextmanager
    def collect_cato_run_timing(self) -> Iterator[None]:
        with self._collect_event_timing("Cato Run"):
            yield

    @contextmanager
    def collect_create_run_timing(self) -> Iterator[None]:
        with self._collect_event_timing("Create run in DB"):
            yield

    @contextmanager
    def collect_suite_timing(self, suite_name: str) -> Iterator[None]:
        with self._collect_event_timing(
            f"Suite {suite_name}",
        ):
            yield

    @contextmanager
    def collect_test_timing(self, test_identifier: TestIdentifier) -> Iterator[None]:
        with self._collect_event_timing(
            f"Test {test_identifier}",
        ):
            yield

    @contextmanager
    def collect_test_command_execution_timing(self) -> Iterator[None]:
        with self._collect_event_timing("test command execution"):
            yield

    @contextmanager
    def collect_image_upload_timing(self, image_type: ImageType) -> Iterator[None]:
        with self._collect_event_timing(f"upload {image_type.name.lower()} image"):
            yield

    @contextmanager
    def collect_image_comparison_timing(self) -> Iterator[None]:
        with self._collect_event_timing("image comparison"):
            yield

    @contextmanager
    def collect_start_test_request_timing(self) -> Iterator[None]:
        with self._collect_event_timing("start test request"):
            yield

    @contextmanager
    def collect_report_test_result(self) -> Iterator[None]:
        with self._collect_event_timing("report test result"):
            yield

    @contextmanager
    def collect_finish_test_timing(self) -> Iterator[None]:
        with self._collect_event_timing("finish test"):
            yield

    @contextmanager
    def collect_upload_log_output_timing(self) -> Iterator[None]:
        with self._collect_event_timing("upload log output"):
            yield

    def get_json_trace(self) -> str:
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

    def get_collected_event_names(self) -> Set[str]:
        names = set()
        for event in self._events:
            names.add(event.name)
        return names

    def _current_microseconds(self) -> float:
        return time.time() * 1000000

    def _current_timestamp(self) -> float:
        return self._current_microseconds() - self._start_time

    def _produce_duration_start_event(self, name: str) -> ChromiumTracingDurationEvent:
        return ChromiumTracingDurationEvent(
            name=name,
            timestamp=self._current_timestamp(),
            type=ChromiumTracingDurationEventType.BEGIN,
        )

    @contextmanager
    def _collect_event_timing(self, event_name: str) -> Iterator[None]:
        start_event = self._produce_duration_start_event(event_name)
        self._events.append(start_event)

        yield

        finish_event = dataclasses.replace(
            start_event,
            type=ChromiumTracingDurationEventType.END,
            timestamp=self._current_timestamp(),
        )
        self._events.append(finish_event)
