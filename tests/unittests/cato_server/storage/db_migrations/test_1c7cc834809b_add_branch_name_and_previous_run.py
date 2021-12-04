import pytest
from sqlalchemy.exc import IntegrityError

from cato_server.configuration.storage_configuration import StorageConfiguration
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator


@pytest.fixture
def revision_eae298066911_before_add_branch_name_and_previous_run(
    mapped_db_connection_string, engine
):
    db_migrator = DbMigrator(
        StorageConfiguration(
            file_storage_url="", database_url=mapped_db_connection_string
        )
    )
    db_migrator.migrate("eae298066911")

    def insert_project(name):
        return connection.execute(
            f"INSERT INTO project_entity (name) VALUES('{name}')"
        ).lastrowid

    def insert_run(project_id):
        return connection.execute(
            f"INSERT INTO run_entity (project_entity_id,started_at) VALUES({project_id},CURRENT_TIMESTAMP)"
        ).lastrowid

    with engine.connect() as connection:
        project_1_id = insert_project("project_1")
        project_2_id = insert_project("project_2")

        run_1 = insert_run(project_1_id)
        run_2 = insert_run(project_2_id)
        run_3 = insert_run(project_1_id)
        run_4 = insert_run(project_2_id)
        run_5 = insert_run(project_1_id)
        run_6 = insert_run(project_2_id)

    return [project_1_id, project_2_id], [run_1, run_2, run_3, run_4, run_5, run_6]


def test_upgrade_add_branch_name_and_previous_run(
    revision_eae298066911_before_add_branch_name_and_previous_run,
    mapped_db_connection_string,
    engine,
):
    db_migrator = DbMigrator(
        StorageConfiguration(
            file_storage_url="", database_url=mapped_db_connection_string
        )
    )
    db_migrator.migrate("1c7cc834809b")

    with engine.connect() as connection:
        _verify_branch_name_is_default_everywhere(connection)

        _verify_branch_name_is_required_and_previous_run_id_not(
            connection, revision_eae298066911_before_add_branch_name_and_previous_run
        )

        _verify_runs_are_linked_correctly(connection)


def _verify_branch_name_is_default_everywhere(connection):
    assert connection.execute("select distinct branch_name from run_entity").all() == [
        ("default",)
    ]


def _verify_branch_name_is_required_and_previous_run_id_not(
    connection, revision_eae298066911_before_add_branch_name_and_previous_run
):
    connection.execute(
        f"INSERT INTO run_entity (project_entity_id,started_at, branch_name) VALUES({revision_eae298066911_before_add_branch_name_and_previous_run[0][0]},CURRENT_TIMESTAMP, 'my_branch_name')"
    )
    with pytest.raises(IntegrityError):
        connection.execute(
            f"INSERT INTO run_entity (project_entity_id,started_at) VALUES({revision_eae298066911_before_add_branch_name_and_previous_run[0][0]},CURRENT_TIMESTAMP)"
        )


def _verify_runs_are_linked_correctly(connection):
    def previous_run_id_by_id(run_id):
        return connection.execute(
            f"select previous_run_id from run_entity where id={run_id}"
        ).all()

    assert previous_run_id_by_id(1) == [(None,)]
    assert previous_run_id_by_id(2) == [(None,)]
    assert previous_run_id_by_id(3) == [(1,)]
    assert previous_run_id_by_id(4) == [(2,)]
    assert previous_run_id_by_id(5) == [(3,)]
    assert previous_run_id_by_id(6) == [(4,)]
