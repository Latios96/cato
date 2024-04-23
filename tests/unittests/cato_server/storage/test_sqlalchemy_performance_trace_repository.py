from cato_common.domain.performance_trace import PerformanceTrace


def test_save(sqlalchemy_performance_trace_repository):
    saved_trace = sqlalchemy_performance_trace_repository.save(
        PerformanceTrace(id=0, performance_trace_json="""{"traceEvents":[]}""")
    )
    assert saved_trace.id == 1
    assert saved_trace.performance_trace_json


def test_find_by_id(sqlalchemy_performance_trace_repository, performance_trace):
    found_trace = sqlalchemy_performance_trace_repository.find_by_id(
        performance_trace.id
    )

    assert found_trace == performance_trace
