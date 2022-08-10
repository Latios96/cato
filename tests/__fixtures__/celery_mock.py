import datetime
import traceback
import uuid

import mock.mock


class MockAsyncResult:
    def __init__(self, task_id, app, status, result, traceback_str):
        self._task_id = task_id
        self._app = app
        self._status = status
        self._result = result
        self._traceback_str = traceback_str

    @property
    def task_id(self):
        return self._task_id

    @property
    def result(self):
        return self._result

    @property
    def state(self):
        return self._status

    @property
    def traceback(self):
        return self._traceback_str


class MockCeleryApp:
    def __init__(self):
        self.results = {}
        self.backend = mock.MagicMock()
        self.backend.get_task_meta.side_effect = self.results.get
        self.backend.meta_from_decoded.side_effect = lambda x: x

    def task(self, *args, **opts):
        callable = args[0]
        # todo assert this is a callable
        app = self

        class WrapCls:
            def delay(self, *args, **opts) -> MockAsyncResult:
                task_id = str(uuid.uuid4())
                try:
                    result = callable(*args, **opts)
                except Exception as e:
                    app.results[task_id] = {
                        "task_id": id,
                        "status": "FAILURE",
                        "result": None,
                        "traceback": traceback.format_exc(),
                        "date_done": datetime.datetime.utcnow(),
                    }
                    return MockAsyncResult(
                        task_id, app, "FAILURE", None, traceback.format_exc()
                    )
                app.results[task_id] = {
                    "task_id": id,
                    "status": "SUCCESS",
                    "result": result,
                    "traceback": None,
                    "date_done": datetime.datetime.utcnow(),
                }
                return MockAsyncResult(task_id, app, "SUCCESS", result, None)

        return WrapCls()
