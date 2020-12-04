from dataclasses import dataclass


@dataclass
class LoggingConfiguration:
    use_file_handler: bool
    max_bytes: int
    backup_count: int
