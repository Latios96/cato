from cato_api_models.catoapimodels import (
    CreateFullRunDto,
    TestSuiteForRunCreation,
    TestForRunCreation,
    MachineInfoDto,
)
from cato_server.domain.event import Event
from cato_server.queues.abstract_message_queue import AbstractMessageQueue
from cato_server.storage.sqlalchemy.sqlalchemy_run_repository import (
    SqlAlchemyRunRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)
from cato_server.usecases.create_full_run import CreateFullRunUsecase
from tests.utils import mock_safe


def test_should_create(sessionmaker_fixture, project):
    run_repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    suite_result_repository = SqlAlchemySuiteResultRepository(sessionmaker_fixture)
    test_result_repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    mock_message_queue = mock_safe(AbstractMessageQueue)
    usecase = CreateFullRunUsecase(
        run_repository,
        suite_result_repository,
        test_result_repository,
        mock_message_queue,
    )

    run = usecase.create_full_run(
        CreateFullRunDto(
            project_id=project.id,
            test_suites=[
                TestSuiteForRunCreation(
                    suite_name="my_suite",
                    suite_variables={},
                    tests=[
                        TestForRunCreation(
                            MachineInfoDto(cpu_name="test", cores=8, memory=8),
                            "cmd",
                            "test/identifier",
                            "test_name",
                            {},
                        )
                    ],
                )
            ],
        )
    )

    assert run.id == 1
    assert run.started_at
    mock_message_queue.send_event.assert_called_with(
        "run_events", str(project.id), Event("RUN_CREATED", run), usecase._run_mapper
    )
