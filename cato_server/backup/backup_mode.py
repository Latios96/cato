from enum import Enum


class BackupMode(Enum):
    FULL = "FULL"
    ONLY_DATABASE = "ONLY_DATABASE"
    ONLY_FILESTORAGE = "ONLY_FILESTORAGE"
