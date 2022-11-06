import uuid

import pytest
from sqlalchemy.exc import OperationalError

from cato_server.configuration.parts.storage_configuration import StorageConfiguration
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator


@pytest.fixture
def revision_7a69c3f1d789_run_batch_add_created_at_column(
    mapped_db_connection_string, engine
):
    db_migrator = DbMigrator(
        StorageConfiguration(
            file_storage_url="", database_url=mapped_db_connection_string
        )
    )
    db_migrator.migrate("7a69c3f1d789")

    def insert_project(name):
        if "sqlite" in mapped_db_connection_string:
            return connection.execute(
                f"INSERT INTO project_entity (name) VALUES('{name}')"
            ).lastrowid
        return connection.execute(
            f"INSERT INTO project_entity (name) VALUES('{name}') RETURNING id"
        ).first()[0]

    def insert_run_batch(project_id):
        insert_statement = f"INSERT INTO run_batch_entity (project_entity_id, provider, run_name, run_identifier,created_at) VALUES({project_id}, 'LOCAL_COMPUTER', 'unknown', '{str(uuid.uuid4())}',CURRENT_TIMESTAMP)"
        if "sqlite" in mapped_db_connection_string:
            return connection.execute(insert_statement).lastrowid
        return connection.execute(f"{insert_statement} RETURNING id").first()[0]

    def insert_run(project_id, run_batch_id):
        insert_statement = f"INSERT INTO run_entity (project_entity_id,started_at,branch_name,run_batch_entity_id) VALUES({project_id},CURRENT_TIMESTAMP,'main', {run_batch_id})"
        if "sqlite" in mapped_db_connection_string:
            return connection.execute(insert_statement).lastrowid
        return connection.execute(f"{insert_statement} RETURNING id").first()[0]

    with engine.connect() as connection:
        project_id = insert_project("project_1")
        run_batch_id = insert_run_batch(project_id)
        run = insert_run(project_id, run_batch_id)

    return project_id, run_batch_id, run


def _verify_column_started_at_not_exists_anymore(
    mapped_db_connection_string, connection, project_id, run_batch_id
):
    with pytest.raises(OperationalError):
        insert_statement = f"INSERT INTO run_entity (project_entity_id,started_at,branch_name,run_batch_entity_id) VALUES({project_id},CURRENT_TIMESTAMP,'main', {run_batch_id})"
        if "sqlite" in mapped_db_connection_string:
            return connection.execute(insert_statement).lastrowid
        return connection.execute(f"{insert_statement} RETURNING id").first()[0]


def _verify_column_created_at_exists(
    mapped_db_connection_string, connection, project_id, run_batch_id
):
    insert_statement = f"INSERT INTO run_entity (project_entity_id,created_at,branch_name,run_batch_entity_id) VALUES({project_id},CURRENT_TIMESTAMP,'main', {run_batch_id})"
    if "sqlite" in mapped_db_connection_string:
        return connection.execute(insert_statement).lastrowid
    return connection.execute(f"{insert_statement} RETURNING id").first()[0]


def test_run_batch_add_created_at_column(
    revision_7a69c3f1d789_run_batch_add_created_at_column,
    mapped_db_connection_string,
    engine,
):
    (
        project_id,
        run_batch_id,
        run_id,
    ) = revision_7a69c3f1d789_run_batch_add_created_at_column

    db_migrator = DbMigrator(
        StorageConfiguration(
            file_storage_url="", database_url=mapped_db_connection_string
        )
    )
    db_migrator.migrate("9a2d397907ef")

    with engine.connect() as connection:
        _verify_column_started_at_not_exists_anymore(
            mapped_db_connection_string, connection, project_id, run_batch_id
        )
        _verify_column_created_at_exists(
            mapped_db_connection_string, connection, project_id, run_batch_id
        )
