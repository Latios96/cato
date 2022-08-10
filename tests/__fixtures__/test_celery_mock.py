import json

from celery.result import AsyncResult

from cato_common.domain.tasks.task_result import TaskResult, TaskResultState
from cato_server.task_queue.task_result_factory import TaskResultFactory
from tests.__fixtures__.celery_mock import MockCeleryApp


def test_submit_successful_task():
    app = MockCeleryApp()

    @app.task
    def my_hello(name):
        return f"Hello {name}"

    async_result = my_hello.delay("Horst")

    assert async_result.result == "Hello Horst"


def test_submit_failing_task():
    app = MockCeleryApp()

    @app.task
    def my_failure():
        raise RuntimeError("Error")

    async_result = my_failure.delay("Horst")

    assert async_result.result is None
    assert async_result.traceback is not None


def test_successful_mocked_async_result_should_work_with_task_result_factory(
    app_and_config_fixture, object_mapper
):
    app, config = app_and_config_fixture
    task_result_factory = TaskResultFactory(config, object_mapper)
    app = MockCeleryApp()

    @app.task
    def my_hello(name):
        return json.dumps({"Hello": name})

    async_result = my_hello.delay("Horst")
    task_result = task_result_factory.from_async_result(async_result)

    assert task_result == TaskResult(
        task_id=async_result.task_id,
        state=TaskResultState.SUCCESS,
        url=f"http://127.0.0.1:{config.port}/api/v1/result/{async_result.task_id}",
        result_={"Hello": "Horst"},
        error_message_=None,
    )


def test_failed_mocked_async_result_should_work_with_task_result_factory(
    app_and_config_fixture, object_mapper
):
    app, config = app_and_config_fixture
    task_result_factory = TaskResultFactory(config, object_mapper)
    app = MockCeleryApp()

    @app.task
    def my_failure():
        raise RuntimeError("Error")

    async_result = my_failure.delay()
    task_result = task_result_factory.from_async_result(async_result)

    assert task_result == TaskResult(
        task_id=async_result.task_id,
        state=TaskResultState.FAILURE,
        url=f"http://127.0.0.1:{config.port}/api/v1/result/{async_result.task_id}",
        result_=None,
        error_message_="RuntimeError: Error",
    )


def test_successful_celeryasync_result_should_work_with_task_result_factory(
    app_and_config_fixture, object_mapper
):
    app, config = app_and_config_fixture
    task_result_factory = TaskResultFactory(config, object_mapper)
    app = MockCeleryApp()

    @app.task
    def my_hello(name):
        return json.dumps({"Hello": name})

    mocked_async_result = my_hello.delay("Horst")
    celery_async_result = AsyncResult(mocked_async_result.task_id, app=app)
    task_result = task_result_factory.from_async_result(celery_async_result)

    assert task_result == TaskResult(
        task_id=mocked_async_result.task_id,
        state=TaskResultState.SUCCESS,
        url=f"http://127.0.0.1:{config.port}/api/v1/result/{mocked_async_result.task_id}",
        result_={"Hello": "Horst"},
        error_message_=None,
    )


def test_failed_celeryasync_result_should_work_with_task_result_factory(
    app_and_config_fixture, object_mapper
):
    app, config = app_and_config_fixture
    task_result_factory = TaskResultFactory(config, object_mapper)
    app = MockCeleryApp()

    @app.task
    def my_failure():
        raise RuntimeError("Error")

    mocked_async_result = my_failure.delay()
    celery_async_result = AsyncResult(mocked_async_result.task_id, app=app)
    task_result = task_result_factory.from_async_result(celery_async_result)

    assert task_result == TaskResult(
        task_id=mocked_async_result.task_id,
        state=TaskResultState.FAILURE,
        url=f"http://127.0.0.1:{config.port}/api/v1/result/{mocked_async_result.task_id}",
        result_=None,
        error_message_="RuntimeError: Error",
    )
