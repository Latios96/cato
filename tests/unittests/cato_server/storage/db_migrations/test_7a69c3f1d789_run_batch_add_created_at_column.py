import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from cato_server.configuration.parts.storage_configuration import StorageConfiguration
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator


@pytest.fixture
def revision_6332525ea212_run_information_change_run_id_to_html(
    mapped_db_connection_string, engine
):
    db_migrator = DbMigrator(
        StorageConfiguration(
            file_storage_url="", database_url=mapped_db_connection_string
        )
    )
    db_migrator.migrate("6332525ea212")

    def insert_project(name):
        if "sqlite" in mapped_db_connection_string:
            return connection.execute(
                f"INSERT INTO project_entity (name) VALUES('{name}')"
            ).lastrowid
        return connection.execute(
            f"INSERT INTO project_entity (name) VALUES('{name}') RETURNING id"
        ).first()[0]

    def insert_run_batch(project_id):
        insert_statement = f"INSERT INTO run_batch_entity (project_entity_id, provider, run_name, run_identifier) VALUES({project_id}, 'LOCAL_COMPUTER', 'unknown', '{str(uuid.uuid4())}')"
        if "sqlite" in mapped_db_connection_string:
            return connection.execute(insert_statement).lastrowid
        return connection.execute(f"{insert_statement} RETURNING id").first()[0]

    with engine.connect() as connection:
        project_id = insert_project("project_1")
        run_batch_id = insert_run_batch(project_id)

    return project_id, run_batch_id


def _verify_run_batch_created_at(connection, run_batch_id):
    assert connection.execute(
        f"select created_at from run_batch_entity where id={run_batch_id}"
    ).first()[0]


def _verify_created_at_is_not_nullable(connection, project_id):
    with pytest.raises(IntegrityError):
        connection.execute(
            f"INSERT INTO run_batch_entity (project_entity_id, provider, run_name, run_identifier) VALUES({project_id}, 'LOCAL_COMPUTER', 'unknown', '{str(uuid.uuid4())}')"
        )

    connection.execute(
        f"INSERT INTO run_batch_entity (project_entity_id, provider, run_name, run_identifier, created_at) VALUES({project_id}, 'LOCAL_COMPUTER', 'unknown', '{str(uuid.uuid4())}', CURRENT_TIMESTAMP)"
    )


def test_run_batch_add_created_at_column(
    revision_6332525ea212_run_information_change_run_id_to_html,
    mapped_db_connection_string,
    engine,
):
    (
        project_id,
        run_batch_id,
    ) = revision_6332525ea212_run_information_change_run_id_to_html

    db_migrator = DbMigrator(
        StorageConfiguration(
            file_storage_url="", database_url=mapped_db_connection_string
        )
    )
    db_migrator.migrate("7a69c3f1d789")

    with engine.connect() as connection:
        _verify_run_batch_created_at(connection, run_batch_id)
        _verify_created_at_is_not_nullable(connection, project_id)
