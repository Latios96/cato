from typing import Optional

from cato_common.domain.output import Output
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class OutputRepository(AbstractRepository[Output, int]):
    def find_by_test_result_id(self, id) -> Optional[Output]:
        raise NotImplementedError()
