import json

import pytest

from cato_server.configuration.storage_configuration import StorageConfiguration
from cato_server.storage.sqlalchemy.migrations.db_migrator import DbMigrator

CONFIG_TEMPLATE = {
    "project_name": "Example",
    "suites": [
        {
            "name": "My_first_test_Suite",
            "tests": [
                {"name": "My_first_test", "command": "python --version"},
            ],
        }
    ],
}

CONVERTED_CONFIG_TEMPLATE = {
    "project_name": "Example",
    "suites": [
        {
            "name": "My_first_test_Suite",
            "tests": [
                {"name": "My_first_test", "command": "python --version"},
            ],
        }
    ],
}


@pytest.fixture
def revision_3984bd2a425d_before_camel_case_conversion(
    mapped_db_connection_string, engine
):
    db_migrator = DbMigrator(
        StorageConfiguration(
            file_storage_url="", database_url=mapped_db_connection_string
        )
    )
    db_migrator.migrate("3984bd2a425d")

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
                f"INSERT INTO run_entity (project_entity_id,started_at,branch_name) VALUES({project_id},CURRENT_TIMESTAMP,'default')"
            ).lastrowid
        return connection.execute(
            f"INSERT INTO run_entity (project_entity_id,started_at) VALUES({project_id},CURRENT_TIMESTAMP) RETURNING id"
        ).first()[0]

    def insert_submission_info(run_id):
        connection.execute(
            f"INSERT INTO submission_info_entity (run_entity_id,config,resource_path,executable) VALUES({run_id}, '{json.dumps(CONFIG_TEMPLATE)}', 'test', 'test')"
        )

    with engine.connect() as connection:
        project_1_id = insert_project("project_1")

        run_1 = insert_run(project_1_id)

        insert_submission_info(run_1)


def test_upgrade_submission_info_camel_case_conversion(
    revision_3984bd2a425d_before_camel_case_conversion,
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
        assert connection.execute(
            "select config from submission_info_entity"
        ).all() == [(json.dumps(CONVERTED_CONFIG_TEMPLATE),)]
