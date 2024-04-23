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


def test_find_by_run_id_should_find(
    sqlalchemy_performance_trace_repository,
    sqlalchemy_run_repository,
    run,
    performance_trace,
):
    run.performance_trace_id = performance_trace.id
    sqlalchemy_run_repository.save(run)

    found_trace = sqlalchemy_performance_trace_repository.find_by_run_id(run.id)

    assert found_trace == performance_trace


def test_find_by_run_id_should_not_find(sqlalchemy_performance_trace_repository, run):
    found_trace = sqlalchemy_performance_trace_repository.find_by_run_id(run.id)

    assert found_trace is None
