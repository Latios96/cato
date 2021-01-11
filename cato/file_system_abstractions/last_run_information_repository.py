import json
import os
from dataclasses import dataclass
from typing import Optional


@dataclass
class LastRunInformation:
    last_run_id: int


class LastRunInformationRepository:
    def __init__(self, path):
        self._path = path

    def write_last_run_information(self, last_run_information: LastRunInformation):
        path = self._last_run_information_path()

        data = {"last_run_id": last_run_information.last_run_id}

        with open(path, "w") as f:
            json.dump(data, f)

    def read_last_run_information(self) -> Optional[LastRunInformation]:
        path = self._last_run_information_path()

        if not os.path.exists(path):
            return None

        with open(path, "r") as f:
            data = json.load(f)

        last_run_id = data.get("last_run_id")
        if last_run_id:
            return LastRunInformation(last_run_id)

    def _last_run_information_path(self):
        return os.path.join(self._path, ".cato_last_run.json")
