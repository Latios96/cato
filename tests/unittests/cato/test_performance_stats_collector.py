import json

import pytest

from cato.reporter.performance_stats_collector import (
    PerformanceStatsCollector,
    ImageType,
)
from cato_common.domain.test_identifier import TestIdentifier


def _verify_collected_events(events):
    assert len(events) == 2

    first_event = events[0]
    second_event = events[1]
    assert first_event.name == second_event.name
    assert second_event.timestamp >= first_event.timestamp


@pytest.mark.parametrize(
    "collect_func",
    [
        "collect_cato_run_timing",
        "collect_create_run_timing",
        "collect_test_command_execution_timing",
        "collect_image_comparison_timing",
        "collect_start_test_request_timing",
        "collect_report_test_result",
        "collect_finish_test_timing",
        "collect_upload_log_output_timing",
    ],
)
def test_collect_functions_no_args(collect_func):
    performance_stats_collector = PerformanceStatsCollector()

    with getattr(performance_stats_collector, collect_func)():
        pass

    _verify_collected_events(performance_stats_collector._events)


class TestCollectFunctionsWithArgs:

    def test_collect_collect_suite_timing(self):
        performance_stats_collector = PerformanceStatsCollector()

        with performance_stats_collector.collect_suite_timing("suite name"):
            pass

        _verify_collected_events(performance_stats_collector._events)

    def test_collect_collect_test_timing(self):
        performance_stats_collector = PerformanceStatsCollector()

        with performance_stats_collector.collect_test_timing(
            TestIdentifier("suite", "test")
        ):
            pass

        _verify_collected_events(performance_stats_collector._events)

    def test_collect_image_upload_timing(self):
        performance_stats_collector = PerformanceStatsCollector()

        with performance_stats_collector.collect_image_upload_timing(ImageType.DIFF):
            pass

        _verify_collected_events(performance_stats_collector._events)


def test_get_json_trace():
    performance_stats_collector = PerformanceStatsCollector()

    with performance_stats_collector.collect_cato_run_timing():
        pass
    json_trace = performance_stats_collector.get_json_trace()
    assert json_trace.startswith(
        '{"traceEvents":[{'
    ), "JSON string should not contain unnecessary whitespaces"
    json_trace = json.loads(json_trace)
    for event in json_trace["traceEvents"]:
        ts = event.pop("ts")
        assert ts < 100
    assert json_trace == {
        "traceEvents": [
            {
                "name": "Cato Run",
                "ph": "B",
                "pid": 0,
                "tid": 0,
            },
            {
                "name": "Cato Run",
                "ph": "E",
                "pid": 0,
                "tid": 0,
            },
        ]
    }


def test_get_collected_event_names():
    performance_stats_collector = PerformanceStatsCollector()

    with performance_stats_collector.collect_cato_run_timing():
        pass
    with performance_stats_collector.collect_create_run_timing():
        pass
    with performance_stats_collector.collect_create_run_timing():
        pass

    assert performance_stats_collector.get_collected_event_names() == {
        "Cato Run",
        "Create run in DB",
    }
