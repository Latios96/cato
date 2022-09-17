"""add run_batch_id to run_entity

Revision ID: ad25c3ecb21e
Revises: 80ef9d93643b
Create Date: 2022-09-16 12:10:27.857617

"""
import uuid

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "ad25c3ecb21e"
down_revision = "80ef9d93643b"
branch_labels = None
depends_on = None


def _insert_run_batch(connection, is_sqlite, project_id):
    insert_statement = f"INSERT INTO run_batch_entity (project_entity_id, provider, run_name, run_identifier) VALUES({project_id}, 'LOCAL_COMPUTER', 'unknown', '{str(uuid.uuid4())}')"
    if is_sqlite:
        return connection.execute(insert_statement).lastrowid
    return connection.execute(f"{insert_statement} RETURNING id").first()[0]


def upgrade():
    with op.batch_alter_table("run_entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "run_batch_entity_id",
                sa.Integer(),
                sa.ForeignKey("run_batch_entity.id", name="run_batch_entity_id_fk"),
                nullable=True,
            ),
        )

    conn = op.get_bind()

    runs = conn.execute("select id, project_entity_id from run_entity").fetchall()
    for run in runs:
        run_id = run[0]
        project_id = run[1]
        run_batch_id = _insert_run_batch(
            conn, "sqlite" in op.get_bind().engine.driver, project_id
        )
        conn.execute(
            f"UPDATE run_entity set run_batch_entity_id={run_batch_id} where id={run_id}"
        )

    with op.batch_alter_table("run_entity", schema=None) as batch_op:
        batch_op.alter_column(
            "run_batch_entity_id", existing_type=sa.String(), nullable=False
        )


def downgrade():
    with op.batch_alter_table("run_entity_id") as batch_op:
        batch_op.drop_column("run_batch_entity_id")
