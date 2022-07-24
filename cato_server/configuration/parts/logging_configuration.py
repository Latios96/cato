from dataclasses import dataclass


@dataclass
class LoggingConfiguration:
    log_file_path: str
    use_file_handler: bool
    max_bytes: int
    backup_count: int
