import logging
import os.path

from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.sqlalchemy.sqlalchemy_simple_file_storage import _FileMapping

CHUNK_SIZE = 2000

logger = logging.getLogger(__name__)


class PopulateByteCountCommand:
    def __init__(self, session_maker, file_storage: AbstractFileStorage):
        self._session_maker = session_maker
        self._file_storage = file_storage

    def populate_byte_count(self):
        session = self._session_maker()
        processed_total = 0
        processed = 0
        populated_entities = 0
        for mapped_entity in session.query(_FileMapping).yield_per(CHUNK_SIZE):
            processed_total += 1
            processed += 1
            if mapped_entity.byte_count:
                continue
            domain_object = self._file_storage.to_domain_object(mapped_entity)
            file_path = self._file_storage.get_path(domain_object)
            if not os.path.exists(file_path):
                continue
            mapped_entity.byte_count = os.path.getsize(file_path)
            mapped_entity = session.merge(mapped_entity)
            populated_entities += 1
            if processed % CHUNK_SIZE == 0:
                processed = 0
                logger.info(
                    f"Flushing, populated {populated_entities}, processed total {processed_total}"
                )
                session.flush()

        session.flush()
        session.commit()
        session.close()
