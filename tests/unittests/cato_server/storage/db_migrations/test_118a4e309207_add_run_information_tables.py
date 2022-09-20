import uuid

import pytest

from cato_server.configuration.parts.storage_configuration import StorageConfiguration
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator


@pytest.fixture
def revision_ad25c3ecb21e_add_run_batch_id_to_run_entity(
    mapped_db_connection_string, engine
):
    db_migrator = DbMigrator(
        StorageConfiguration(
            file_storage_url="", database_url=mapped_db_connection_string
        )
    )
    db_migrator.migrate("ad25c3ecb21e")

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

    def insert_run(project_id, run_batch_id):
        insert_statement = f"INSERT INTO run_entity (project_entity_id,started_at,branch_name,run_batch_entity_id) VALUES({project_id},CURRENT_TIMESTAMP,'main', {run_batch_id})"
        if "sqlite" in mapped_db_connection_string:
            return connection.execute(insert_statement).lastrowid
        return connection.execute(f"{insert_statement} RETURNING id").first()[0]

    with engine.connect() as connection:
        project_id = insert_project("project_1")
        run_batch_id = insert_run_batch(project_id)
        run_id = insert_run(project_id, run_batch_id)

    return project_id, run_id


def _verify_run_has_run_information(connection, run_id):
    run_information_id = connection.execute(
        f"select id from basic_run_information_entity where run_entity_id={run_id}"
    ).first()[0]
    assert run_information_id == 1
    local_computer_run_information_id = connection.execute(
        f"select id from local_computer_run_information_entity where id={run_id}"
    ).first()[0]
    assert local_computer_run_information_id == 1


def test_add_run_information_tables(
    mapped_db_connection_string,
    engine,
    revision_ad25c3ecb21e_add_run_batch_id_to_run_entity,
):
    project_id, run_id = revision_ad25c3ecb21e_add_run_batch_id_to_run_entity

    db_migrator = DbMigrator(
        StorageConfiguration(
            file_storage_url="", database_url=mapped_db_connection_string
        )
    )
    db_migrator.migrate("118a4e309207")

    with engine.connect() as connection:
        _verify_run_has_run_information(connection, run_id)
