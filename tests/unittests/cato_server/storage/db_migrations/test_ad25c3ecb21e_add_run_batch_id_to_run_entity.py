import pytest
from sqlalchemy.exc import IntegrityError

from cato_server.configuration.parts.storage_configuration import StorageConfiguration
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator


@pytest.fixture
def revision_80ef9d93643b_add_run_batch_table(mapped_db_connection_string, engine):
    db_migrator = DbMigrator(
        StorageConfiguration(
            file_storage_url="", database_url=mapped_db_connection_string
        )
    )
    db_migrator.migrate("80ef9d93643b")

    def insert_project(name):
        if "sqlite" in mapped_db_connection_string:
            return connection.execute(
                f"INSERT INTO project_entity (name) VALUES('{name}')"
            ).lastrowid
        return connection.execute(
            f"INSERT INTO project_entity (name) VALUES('{name}') RETURNING id"
        ).first()[0]

    def insert_run(project_id):
        if "sqlite" in mapped_db_connection_string:
            return connection.execute(
                f"INSERT INTO run_entity (project_entity_id,started_at,branch_name) VALUES({project_id},CURRENT_TIMESTAMP,'main')"
            ).lastrowid
        return connection.execute(
            f"INSERT INTO run_entity (project_entity_id,started_at,branch_name) VALUES({project_id},CURRENT_TIMESTAMP,'main') RETURNING id"
        ).first()[0]

    with engine.connect() as connection:
        project_id = insert_project("project_1")

        run_id = insert_run(project_id)

    return project_id, run_id


def test_add_run_batch_id_to_run_entity(
    mapped_db_connection_string, engine, revision_80ef9d93643b_add_run_batch_table
):
    project_id, run_id = revision_80ef9d93643b_add_run_batch_table

    db_migrator = DbMigrator(
        StorageConfiguration(
            file_storage_url="", database_url=mapped_db_connection_string
        )
    )
    db_migrator.migrate("ad25c3ecb21e")

    with engine.connect() as connection:
        _verify_run_has_run_batch(connection, run_id)
        _verify_run_batch_entity_id_is_not_nullable(connection, project_id)


def _verify_run_has_run_batch(connection, run_id):
    run_batch_id = connection.execute(
        f"select run_batch_entity_id from run_entity where id={run_id}"
    ).first()[0]
    assert run_batch_id == 1


def _verify_run_batch_entity_id_is_not_nullable(connection, project_id):
    with pytest.raises(IntegrityError):
        connection.execute(
            f"INSERT INTO run_entity (project_entity_id,started_at,branch_name) VALUES({project_id},CURRENT_TIMESTAMP,'main')"
        )
