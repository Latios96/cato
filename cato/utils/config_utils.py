import json
import os
from typing import Optional, Dict


class UrlMissingException(Exception):
    def __init__(self, path: str):
        super(UrlMissingException, self).__init__(
            f'No server url was given. Provide one with -u/--url or add a "serverUrl" entry to {path}'
        )


def resolve_config_path(path: Optional[str]) -> str:
    if not path:
        path = os.getcwd()
    path = os.path.abspath(path)
    if os.path.isdir(path):
        path = os.path.join(path, "cato.json")
    return path


def read_url_from_config_path(path: Optional[str], require_url: bool) -> str:
    resolved_config_path = resolve_config_path(path)
    if not os.path.exists(resolved_config_path):
        return "<not given>"
    with open(resolved_config_path) as f:
        config: Dict[str, str] = json.load(f)
    config_from_url = config.get("serverUrl")
    if config_from_url:
        return config_from_url
    if require_url:
        raise UrlMissingException(resolved_config_path)
    return "<not given>"
