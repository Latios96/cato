import hashlib
import logging
import os
from typing import IO, Tuple, AnyStr

from cato_server.domain.file import File
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_simple_file_storage import (
    _FileMapping,
)

logger = logging.getLogger(__name__)


class SqlAlchemyDeduplicatingFileStorage(
    AbstractSqlAlchemyRepository[File, _FileMapping, int], AbstractFileStorage
):
    def __init__(self, session_maker, root_path: str, hash_calculatur=hashlib.sha3_256):
        super(SqlAlchemyDeduplicatingFileStorage, self).__init__(session_maker)
        self._root_path = root_path
        self._hash_calculatur = hash_calculatur

    def save_file(self, path: str) -> File:
        file, content = self._create_file_obj_for_path(path)

        needs_write, value_counter = self._needs_write(file, content)
        file.value_counter = value_counter

        if needs_write:
            logger.info("Write file %s to storage at %s..", path, self.get_path(file))
            target_stream = self._get_write_stream(file)
            target_stream.write(content)
            target_stream.close()
        logger.info("Writing done, saving file %s..", file)
        file = self.save(file)
        return file

    def save_stream(self, name: str, stream: IO) -> File:
        file, content = self._create_file_obj_for_stream(name, stream)

        needs_write, value_counter = self._needs_write(file, content)
        file.value_counter = value_counter

        if needs_write:
            logger.info("Writing stream to storage at %s..", self.get_path(file))
            target_stream = self._get_write_stream(file)
            target_stream.write(content)
            target_stream.close()

        logger.info("Writing done, saving file %s..", file)
        file = self.save(file)
        return file

    def get_read_stream(self, file: File) -> IO:
        return open(self.get_path(file), "rb")

    def _create_file_obj_for_stream(self, name: str, stream: IO) -> Tuple[File, AnyStr]:
        bytes = stream.read()
        file_hash = self._hash_calculatur(bytes).hexdigest()
        return File(id=0, name=name, hash=str(file_hash), value_counter=0), bytes

    def _create_file_obj_for_path(self, path: str) -> Tuple[File, AnyStr]:
        with open(path, "rb") as f:
            return self._create_file_obj_for_stream(os.path.basename(path), f)

    def to_entity(self, domain_object: File) -> _FileMapping:
        return _FileMapping(
            id=domain_object.id if domain_object.id else None,
            name=domain_object.name,
            hash=domain_object.hash,
        )

    def to_domain_object(self, entity: _FileMapping) -> File:
        return File(id=entity.id, name=entity.name, hash=entity.hash, value_counter=0)

    def mapping_cls(self):
        return _FileMapping

    def _get_write_stream(self, file: File) -> IO:
        return open(self.get_path(file), "wb")

    def get_path(self, file: File) -> str:
        target_path = os.path.join(
            self._get_bucket_folder(file.hash),
            str(file.value_counter) + os.path.splitext(file.name)[1],
        )
        target_dir = os.path.dirname(target_path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        return target_path

    def _needs_write(self, file, content):
        needs_write = not os.path.exists(self._get_bucket_folder(file.hash))
        if needs_write:
            logger.info(
                "File %s needs write, no file exists for hash %s", file, file.hash
            )
            return True, 0

        needs_write = True

        existing_entries = self._existing_entries(file)
        for existing_entry in existing_entries:
            with open(existing_entry, "rb") as f:
                stored_content = f.read()

            if stored_content == content:
                logger.info(
                    "File %s needs no write, file already exists for hash %s at %s",
                    file,
                    file.hash,
                    existing_entry,
                )
                return False, self._get_value_counter_from_path(existing_entry)

        logger.info(
            "File %s should write: %s, no content match for colliding hash %s",
            file,
            needs_write,
            file.hash,
        )
        next_value_counter = self._get_next_value_counter(existing_entries) + 1

        return True, next_value_counter

    def _get_bucket_folder(self, hash):
        return os.path.join(self._root_path, hash)

    def _existing_entries(self, file):
        names = os.listdir(self._get_bucket_folder(file.hash))
        return list(
            map(lambda x: os.path.join(self._get_bucket_folder(file.hash), x), names)
        )

    def _get_next_value_counter(self, existing_entries):
        values = []
        for entry in existing_entries:
            values.append(self._get_value_counter_from_path(entry))
        return max(values)

    def _get_value_counter_from_path(self, path):
        value = os.path.splitext(os.path.basename(path))[0]
        return int(value)
