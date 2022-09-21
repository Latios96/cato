"""add run information tables

Revision ID: 118a4e309207
Revises: ad25c3ecb21e
Create Date: 2022-09-17 16:05:22.890085

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "118a4e309207"
down_revision = "ad25c3ecb21e"
branch_labels = None
depends_on = None


def _insert_basic_information(connection, is_sqlite, run_id):
    insert_statement = f"INSERT INTO basic_run_information_entity (run_entity_id, run_information_type, os, computer_name) VALUES ({run_id}, 'LOCAL_COMPUTER', 'UNKNOWN', 'unknown')"
    if is_sqlite:
        return connection.execute(insert_statement).lastrowid
    return connection.execute(f"{insert_statement} RETURNING id").first()[0]


def upgrade():
    op.create_table(
        "basic_run_information_entity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("run_entity_id", sa.INTEGER, sa.ForeignKey("run_entity.id")),
        sa.Column("run_information_type", sa.String, nullable=False),
        sa.Column("os", sa.String, nullable=False),
        sa.Column("computer_name", sa.String, nullable=False),
    )
    op.create_table(
        "local_computer_run_information_entity",
        sa.Column(
            "id",
            sa.INTEGER,
            sa.ForeignKey("basic_run_information_entity.id"),
            primary_key=True,
        ),
        sa.Column("local_username", sa.String, nullable=False),
    )
    op.create_table(
        "github_actions_run_information_entity",
        sa.Column(
            "id",
            sa.INTEGER,
            sa.ForeignKey("basic_run_information_entity.id"),
            primary_key=True,
        ),
        sa.Column("github_run_id", sa.BIGINT, nullable=False),
        sa.Column("job_id", sa.BIGINT, nullable=False),
        sa.Column("job_name", sa.String, nullable=False),
        sa.Column("actor", sa.String, nullable=False),
        sa.Column("attempt", sa.INTEGER, nullable=False),
        sa.Column("run_number", sa.INTEGER, nullable=False),
        sa.Column("github_url", sa.String, nullable=False),
        sa.Column("github_api_url", sa.String, nullable=False),
    )

    conn = op.get_bind()

    runs = conn.execute("select id from run_entity").fetchall()
    for run in runs:
        run_id = run[0]
        basic_run_id = _insert_basic_information(
            conn, "sqlite" in op.get_bind().engine.driver, run_id
        )

        conn.execute(
            f"INSERT INTO local_computer_run_information_entity (id, local_username) VALUES ({basic_run_id}, 'unknown')"
        )


def downgrade():
    op.drop_table("basic_run_information_entity")
    op.drop_table("local_computer_run_information_entity")
    op.drop_table("github_actions_run_information_entity")
