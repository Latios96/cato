from dataclasses import dataclass


@dataclass
class StorageConfiguration:
    file_storage_url: str
    database_url: str
