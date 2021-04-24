import pytest

from cato_server.domain.execution_status import ExecutionStatus
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.start_test import StartTest
from tests.utils import mock_safe


class TestStartTest:
    def setup_method(self, method):
        self.test_result_repository = mock_safe(TestResultRepository)
        self.start_test_usecase = StartTest(self.test_result_repository)

    def test_starting_a_not_existing_test_should_fail(self):
        self.test_result_repository.find_by_id.return_value = None

        with pytest.raises(ValueError):
            self.start_test_usecase.start_test(42)

        self.test_result_repository.save.assert_not_called()

    def test_starting_an_existing_test_should_set_status_and_start_time(
        self, test_result_factory
    ):
        test_result = test_result_factory()
        test_result.started_at = None
        test_result.execution_status = ExecutionStatus.NOT_STARTED
        self.test_result_repository.find_by_id.return_value = test_result

        self.start_test_usecase.start_test(1)

        self.test_result_repository.save.assert_called_with(test_result)
        assert test_result.execution_status == ExecutionStatus.RUNNING
        assert test_result.started_at is not None
