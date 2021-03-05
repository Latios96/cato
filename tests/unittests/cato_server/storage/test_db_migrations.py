from pathlib import Path
from typing import Optional

import pytest

from cato_server.configuration.storage_configuration import StorageConfiguration
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator


def find_pg_ctl(ver: str) -> Optional[Path]:
    candidates = list(Path(f"/usr/lib/postgresql/{ver}/").glob("**/bin/pg_ctl"))
    if candidates:
        return candidates[0]


def can_not_launch_postgres():
    ctl = find_pg_ctl("12")
    if not ctl:
        return True
    return False


requires_postgres = pytest.mark.skipif(
    can_not_launch_postgres(), reason="No pg_ctl executable found"
)


@requires_postgres
def test_db_migrator(db_connection_string):
    db_migrator = DbMigrator(
        StorageConfiguration(file_storage_url="", database_url=db_connection_string)
    )
    db_migrator.migrate()
