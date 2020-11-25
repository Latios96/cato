import os

from cato.storage.domain.File import File
from cato.storage.sqlalchemy.sqlalchemy_simple_file_storage import (
    SqlAlchemySimpleFileStorage,
)


class SqlAlchemyDeduplicatingFileStorage(SqlAlchemySimpleFileStorage):
    def get_path(self, file: File) -> str:
        target_path = os.path.join(
            self._root_path, file.hash + os.path.splitext(file.name)[1]
        )
        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        return target_path

    def _needs_write(self, file):
        return not os.path.exists(self.get_path(file))
