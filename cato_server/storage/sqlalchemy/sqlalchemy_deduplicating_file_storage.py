import os

from cato_server.storage.domain.file import File
from cato_server.storage.sqlalchemy.sqlalchemy_simple_file_storage import (
    SqlAlchemySimpleFileStorage,
)

import logging

logger = logging.getLogger(__name__)


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
        needs_write = not os.path.exists(self.get_path(file))
        if needs_write:
            logger.info(
                "File %s needs write, no file exists for hash %s", file, file.hash
            )
        else:
            logger.info(
                "File %s needs no write, file exists for hash %s", file, file.hash
            )
        return needs_write
