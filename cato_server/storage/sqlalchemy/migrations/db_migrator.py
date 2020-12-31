import os

from alembic import command
from alembic.config import Config

from cato_server.configuration.storage_configuration import StorageConfiguration


class DbMigrator:
    def __init__(self, storage_configuration: StorageConfiguration):
        self._storage_configuration = storage_configuration

    def migrate(self):
        database_url = self._storage_configuration.database_url

        alembic_cfg = Config(self._alembic_config_path)
        if "sqlite" in database_url:
            pass
        alembic_cfg.set_section_option("alembic", "sqlalchemy.url", database_url)
        alembic_cfg.set_section_option(
            "alembic",
            "script_location",
            os.path.join(os.path.dirname(__file__), "alembic"),
        )
        command.upgrade(alembic_cfg, "head")

    @property
    def _alembic_config_path(self):
        return os.path.join(os.path.dirname(__file__), "alembic_config.ini")

    @property
    def _alembic_scripts_path(self):
        return (
            os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "alembic"
            ),
        )
