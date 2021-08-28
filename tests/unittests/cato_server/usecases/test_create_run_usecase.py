from cato_api_models.catoapimodels import (
    CreateFullRunDto,
    TestSuiteForRunCreation,
    TestForRunCreation,
    MachineInfoDto,
)
from cato_server.configuration.optional_component import OptionalComponent
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
from cato_server.usecases.create_run import CreateRunUsecase
from tests.utils import mock_safe
from cato_api_models.catoapimodels import RunDto, RunStatusDto


def test_should_create(sessionmaker_fixture, project, object_mapper):
    run_repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    suite_result_repository = SqlAlchemySuiteResultRepository(sessionmaker_fixture)
    test_result_repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    mock_message_queue = mock_safe(OptionalComponent[AbstractMessageQueue])
    usecase = CreateRunUsecase(
        run_repository,
        suite_result_repository,
        test_result_repository,
        mock_message_queue,
        object_mapper,
    )

    run = usecase.create_run(
        CreateFullRunDto(
            project_id=project.id,
            test_suites=[
                TestSuiteForRunCreation(
                    suite_name="my_suite",
                    suite_variables={},
                    tests=[
                        TestForRunCreation(
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
    mock_message_queue.component.send_event.assert_called_with(
        "run_events",
        str(project.id),
        Event(
            "RUN_CREATED",
            RunDto(
                id=run.id,
                project_id=run.project_id,
                started_at=run.started_at.isoformat(),
                status=RunStatusDto.NOT_STARTED,
                duration=0,
            ),
        ),
        object_mapper,
    )
    assert test_result_repository.find_by_id(1).machine_info == None
