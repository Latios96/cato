from dataclasses import dataclass


@dataclass
class File:
    id: int
    name: str
    md5_hash: str
