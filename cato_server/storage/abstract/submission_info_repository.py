from cato_server.domain.submission_info import SubmissionInfo
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class SubmissionInfoRepository(AbstractRepository[SubmissionInfo, int]):
    pass
