import os
from typing import Optional


def resolve_config_path(path: Optional[str]) -> str:
    if not path:
        path = os.getcwd()
    path = os.path.abspath(path)
    if os.path.isdir(path):
        path = os.path.join(path, "cato.json")
    return path
