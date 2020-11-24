from typing import IO

from cato.storage.domain.File import File


class AbstractFileStorage:

    def save_file(self, path: str) -> File:
        raise NotImplementedError()

    def save_stream(self, stream: IO) -> File:
        raise NotImplementedError()

    def find_by_id(self, id: int) -> File:
        raise NotImplementedError()

    def get_stream(self, id: int) -> IO:
        raise NotImplementedError()

    def get_path(self, id: int) -> IO:
        raise NotImplementedError()
