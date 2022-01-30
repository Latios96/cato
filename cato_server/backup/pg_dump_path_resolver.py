import glob
import os.path
import platform
import shutil
from typing import Optional


class PgDumpPathResolver:
    def resolve(self, hint: Optional[str]) -> str:
        resolved = self._resolve_hint_and_default_locations(hint)
        if not resolved:
            raise RuntimeError("Could not find a pg_dump executable")
        return resolved

    def _resolve_hint_and_default_locations(self, hint: Optional[str]) -> Optional[str]:
        if hint and os.path.exists(hint):
            return hint

        pg_dump_from_path = shutil.which("pg_dump")
        if pg_dump_from_path is not None:
            return pg_dump_from_path

        if platform.system() == "Windows":
            return self._resolve_windows()

        return None

    def _resolve_windows(self) -> Optional[str]:
        postgres_default_install_location_matches = glob.glob(
            r"C:\Program Files\PostgreSQL\*\bin\pg_dump.exe"
        )
        if postgres_default_install_location_matches:
            return sorted(postgres_default_install_location_matches)[-1]
        return None
