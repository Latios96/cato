import os

import pytest
from alembic import command
from alembic.config import Config


def test_migrations(test_resource_provider):
    config_path = test_resource_provider.resource_by_name(
        "alembic-config-for-tests.ini"
    )
    alembic_cfg = Config(config_path)
    alembic_cfg.set_section_option(
        "alembic",
        "script_location",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(config_path))), "alembic"
        ),
    )

    command.upgrade(alembic_cfg, "head")


@pytest.mark.skip
def test_example_postgres(postgresql, test_resource_provider):
    # requires pytest-postgresql
    connection = f"postgresql+psycopg2://{postgresql.info.user}:@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}"

    config_path = test_resource_provider.resource_by_name(
        "alembic-config-for-tests.ini"
    )
    alembic_cfg = Config(config_path)
    alembic_cfg.set_section_option("alembic", "sqlalchemy.url", connection)
    alembic_cfg.set_section_option(
        "alembic",
        "script_location",
        os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(config_path))), "alembic"
        ),
    )

    command.upgrade(alembic_cfg, "head")
