from fastapi import APIRouter
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from cato_common.mappers.page_mapper import PageMapper
from cato_common.storage.page import PageRequest, Page
from cato_server.api.filter_option_utils import run_filter_options_from_request
from cato_server.api.page_utils import page_request_from_request
from cato_server.storage.abstract.run_batch_repository import RunBatchRepository
from cato_server.usecases.aggregate_run_batch import AggregateRunBatch


class RunBatchBlueprint(APIRouter):
    def __init__(
        self,
        run_batch_repository: RunBatchRepository,
        page_mapper: PageMapper,
        aggregate_run_batch: AggregateRunBatch,
    ):
        super(RunBatchBlueprint, self).__init__()
        self._run_batch_repository = run_batch_repository
        self._page_mapper = page_mapper
        self._aggregate_run_batch = aggregate_run_batch

        self.get("/run_batches/project/{project_id}")(self.run_batches_by_project)

    def run_batches_by_project(self, project_id: int, request: Request) -> Response:
        run_filter_options = run_filter_options_from_request(request.query_params)
        page_request = page_request_from_request(request.query_params)
        if not page_request:
            page_request = PageRequest.first(30)
        run_batches_page = self._run_batch_repository.find_by_project_id_with_paging(
            project_id, page_request, run_filter_options
        )
        if not run_batches_page.entities:
            return JSONResponse(content=self._page_mapper.to_dict(run_batches_page))

        aggregated_run_batches = (
            self._aggregate_run_batch.aggregate_run_batches_by_project_id(
                run_batches_page.entities[0].project_id, run_batches_page.entities
            )
        )
        aggregated_run_batches_page = Page(
            page_number=run_batches_page.page_number,
            page_size=run_batches_page.page_size,
            total_entity_count=run_batches_page.total_entity_count,
            entities=aggregated_run_batches,
        )

        return JSONResponse(
            content=self._page_mapper.to_dict(aggregated_run_batches_page)
        )
