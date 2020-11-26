import hashlib
import os
import shutil
from typing import IO

from sqlalchemy import Column, Integer, String

from cato.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato.storage.domain.File import File
from cato.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class _FileMapping(Base):
    __tablename__ = "file_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    hash = Column(String)


class SqlAlchemySimpleFileStorage(
    AbstractSqlAlchemyRepository[File, _FileMapping, int], AbstractFileStorage
):
    def __init__(self, session_maker, root_path: str):
        super(SqlAlchemySimpleFileStorage, self).__init__(session_maker)
        self._root_path = root_path

    def save_file(self, path: str) -> File:
        file = self._create_file_obj_for_path(path)
        file = self.save(file)
        if self._needs_write(file):
            shutil.copy(path, self.get_path(file))
        return file

    def save_stream(self, name: str, stream: IO) -> File:
        file = self._create_file_obj_for_stream(name, stream)
        file = self.save(file)
        if self._needs_write(file):
            target_stream = self.get_write_stream(file)
            for line in stream:
                target_stream.write(line)
            target_stream.close()
        return file

    def get_write_stream(self, file: File) -> IO:
        return open(self.get_path(file), "wb")

    def get_read_stream(self, file: File) -> IO:
        return open(self.get_path(file), "rb")

    def get_path(self, file: File) -> str:
        target_path = os.path.join(self._root_path, str(file.id), file.name)
        if not os.path.exists(os.path.dirname(target_path)):
            os.makedirs(os.path.dirname(target_path))
        return target_path

    def _create_file_obj_for_stream(self, name: str, stream: IO) -> File:
        bytes = stream.read()
        file_hash = hashlib.sha3_256(bytes).hexdigest()
        return File(id=0, name=name, hash=str(file_hash))

    def _create_file_obj_for_path(self, path: str) -> File:
        with open(path, "rb") as f:
            return self._create_file_obj_for_stream(os.path.basename(path), f)

    def to_entity(self, domain_object: File) -> _FileMapping:
        return _FileMapping(
            id=domain_object.id if domain_object.id else None,
            name=domain_object.name,
            hash=domain_object.hash,
        )

    def to_domain_object(self, entity: _FileMapping) -> File:
        return File(id=entity.id, name=entity.name, hash=entity.hash)

    def mapping_cls(self):
        return _FileMapping

    def _needs_write(self, file):
        return True
