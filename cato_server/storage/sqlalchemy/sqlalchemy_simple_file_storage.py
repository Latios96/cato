import hashlib
import os
import shutil
from typing import IO, Tuple, AnyStr

from sqlalchemy import Column, Integer, String, BigInteger

from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_common.domain.file import File
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)

import logging

logger = logging.getLogger(__name__)


class _FileMapping(Base):
    __tablename__ = "file_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    hash = Column(String)
    value_counter = Column(Integer)
    byte_count = Column(BigInteger)


class SqlAlchemySimpleFileStorage(
    AbstractSqlAlchemyRepository[File, _FileMapping, int], AbstractFileStorage
):
    def __init__(self, session_maker, root_path: str):
        super(SqlAlchemySimpleFileStorage, self).__init__(session_maker)
        self._root_path = root_path

    def save_file(self, path: str) -> File:
        file, content = self._create_file_obj_for_path(path)
        logger.info("Saving file %s..", file)
        file = self.save(file)
        logger.info("Write file %s to storage at %s", path, self.get_path(file))
        target_path = self.get_path(file)
        shutil.copy(path, target_path)
        return file

    def save_stream(self, name: str, stream: IO) -> File:
        file, content = self._create_file_obj_for_stream(name, stream)
        logger.info("Saving file %s..", file)
        file = self.save(file)
        logger.info("Write stream to storage at %s", self.get_path(file))
        target_stream = self._get_write_stream(file)
        target_stream.write(content)
        target_stream.close()
        return file

    def get_read_stream(self, file: File) -> IO:
        return open(self.get_path(file), "rb")

    def get_path(self, file: File) -> str:
        target_path = os.path.join(self._root_path, str(file.id), file.name)
        if not os.path.exists(os.path.dirname(target_path)):
            os.makedirs(os.path.dirname(target_path))
        return target_path

    def _create_file_obj_for_stream(self, name: str, stream: IO) -> Tuple[File, AnyStr]:
        bytes = stream.read()
        byte_count = len(bytes)
        file_hash = hashlib.sha3_256(bytes).hexdigest()
        return (
            File(
                id=0,
                name=name,
                hash=str(file_hash),
                value_counter=0,
                byte_count=byte_count,
            ),
            bytes,
        )

    def _create_file_obj_for_path(self, path: str) -> Tuple[File, AnyStr]:
        with open(path, "rb") as f:
            return self._create_file_obj_for_stream(os.path.basename(path), f)

    def to_entity(self, domain_object: File) -> _FileMapping:
        return _FileMapping(
            id=domain_object.id if domain_object.id else None,
            name=domain_object.name,
            hash=domain_object.hash,
            byte_count=domain_object.byte_count,
        )

    def to_domain_object(self, entity: _FileMapping) -> File:
        return File(
            id=entity.id,
            name=entity.name,
            hash=entity.hash,
            value_counter=0,
            byte_count=entity.byte_count,
        )

    def mapping_cls(self):
        return _FileMapping

    def _get_write_stream(self, file: File) -> IO:
        return open(self.get_path(file), "wb")
