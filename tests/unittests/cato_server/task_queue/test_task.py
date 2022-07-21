from dataclasses import dataclass

from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.task_queue.task import Task, P, R, Void


def test_should_handle_serialization_correctly(object_mapper):
    @dataclass
    class MyTaskParams:
        value: int

    @dataclass
    class MyTaskResult:
        value: int

    class MyTask(Task[MyTaskParams, MyTaskResult]):
        def __init__(self, object_mapper: ObjectMapper):
            super(MyTask, self).__init__(object_mapper, MyTaskParams)

        def _execute(self, params: MyTaskParams) -> MyTaskResult:
            return MyTaskResult(params.value + 1)

    my_task = MyTask(object_mapper)

    result = my_task.execute('{"value": 42}')

    assert result == '{"value": 43}'


def test_should_handle_serialization_correctly_for_void(object_mapper):
    @dataclass
    class MyVoidTaskParams:
        value: int

    class MyTask(Task[MyVoidTaskParams, Void]):
        def __init__(self, object_mapper: ObjectMapper):
            super(MyTask, self).__init__(object_mapper, MyVoidTaskParams)

        def _execute(self, params: MyVoidTaskParams) -> Void:
            return Void()

    my_task = MyTask(object_mapper)

    result = my_task.execute('{"value": 42}')

    assert result == "{}"
