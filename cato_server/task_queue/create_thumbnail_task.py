from dataclasses import dataclass

from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.task_queue.task import Task, Void
from cato_server.usecases.create_thumbnail import CreateThumbnail


@dataclass
class CreateThumbnailParams:
    test_result_id: int


class CreateThumbnailTask(Task):
    def __init__(
        self,
        object_mapper: ObjectMapper,
        test_result_repository: TestResultRepository,
        create_thumbnail: CreateThumbnail,
    ):
        super(CreateThumbnailTask, self).__init__(object_mapper, CreateThumbnailParams)
        self._test_result_repository = test_result_repository
        self._create_thumbnail = create_thumbnail

    def _execute(self, params: CreateThumbnailParams) -> Void:
        test_result = self._test_result_repository.find_by_id(params.test_result_id)
        if not test_result:
            raise RuntimeError(
                "Did not expect to not find a TestResult with id %s in the db.",
                params.test_result_id,
            )

        self._create_thumbnail.create_thumbnail(test_result)

        return Void()
