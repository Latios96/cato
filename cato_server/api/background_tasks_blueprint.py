from fastapi import APIRouter

from cato_server.usecases.fail_timed_out_tests import FailTimedOutTests


class BackgroundTasksBlueprint(APIRouter):
    def __init__(self, fail_timed_out_tests: FailTimedOutTests):
        super(BackgroundTasksBlueprint, self).__init__()
        self._fail_timed_out_tests = fail_timed_out_tests

        self.get("/background_tasks/fail_timed_out_tests")(self.fail_timed_out_tests)

    def fail_timed_out_tests(self):
        self._fail_timed_out_tests.fail_timed_out_tests()
