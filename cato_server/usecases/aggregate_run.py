from cato_common.domain.run import Run
from cato_common.dtos.run_dto import RunDto
from cato_common.storage.page import Page
from cato_server.run_status_calculator import RunStatusCalculator
from cato_server.storage.abstract.test_result_repository import TestResultRepository


class AggregateRun:
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        run_status_calculator: RunStatusCalculator,
    ):
        self._test_result_repository = test_result_repository
        self._run_status_calculator = run_status_calculator

    def aggregate_runs_by_project_id(
        self, project_id: int, run_page: Page[Run]
    ) -> Page[RunDto]:
        status_by_run_id = self._test_result_repository.find_status_by_project_id(
            project_id
        )
        duration_by_run_id = self._test_result_repository.duration_by_run_ids(
            {run.id for run in run_page.entities}
        )

        dtos = []
        for run in run_page.entities:
            status = self._run_status_calculator.calculate(
                status_by_run_id.get(run.id, set())
            )
            dtos.append(
                RunDto(
                    id=run.id,
                    project_id=run.id,
                    started_at=run.started_at,
                    status=status,
                    duration=duration_by_run_id[run.id],
                    branch_name=run.branch_name,
                    run_information=run.run_information,
                )
            )

        return Page(
            page_number=run_page.page_number,
            page_size=run_page.page_size,
            total_entity_count=run_page.total_entity_count,
            entities=dtos,
        )
