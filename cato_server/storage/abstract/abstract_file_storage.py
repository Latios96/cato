from typing import IO, Optional

from cato_server.storage.domain.File import File


class AbstractFileStorage:
    def save_file(self, path: str) -> File:
        raise NotImplementedError()

    def save_stream(self, name: str, stream: IO) -> File:
        raise NotImplementedError()

    def find_by_id(self, id: int) -> Optional[File]:
        raise NotImplementedError()

    def get_read_stream(self, file: File) -> IO:
        raise NotImplementedError()

    def get_path(self, file: File) -> str:
        raise NotImplementedError()
