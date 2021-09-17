from typing import List, Optional

from cato_server.domain.test_edit import TestEdit, EditTypes
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class TestEditRepository(AbstractRepository[TestEdit, int]):
    def find_by_test_id(
        self, test_id: int, edit_type: Optional[EditTypes] = None
    ) -> List[TestEdit]:
        pass

    def find_by_run_id(self, run_id: int) -> List[TestEdit]:
        pass
