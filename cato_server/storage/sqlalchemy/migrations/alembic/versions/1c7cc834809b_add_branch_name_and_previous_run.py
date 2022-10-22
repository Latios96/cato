"""add branch name and previous run

Revision ID: 1c7cc834809b
Revises: eae298066911
Create Date: 2021-12-03 21:34:48.749381

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.

revision = "1c7cc834809b"
down_revision = "eae298066911"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("run_entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "branch_name",
                sa.String(),
                nullable=True,
            ),
        )
        batch_op.add_column(
            sa.Column(
                "previous_run_id",
                sa.Integer(),
                sa.ForeignKey("run_entity.id", name="previous_run_id_run_entity_id_fk"),
                nullable=True,
            ),
        )

    conn = op.get_bind()
    conn.execute("UPDATE run_entity SET branch_name='default'")

    with op.batch_alter_table("run_entity", schema=None) as batch_op:
        batch_op.alter_column("branch_name", existing_type=sa.String(), nullable=False)

    projects = conn.execute("select id from project_entity").fetchall()
    for project in projects:
        project_id = project[0]
        runs = conn.execute(
            f"select id from run_entity where project_entity_id = {project_id} order by id"
        ).fetchall()
        previous_id = None
        for run in runs:
            run_id = run[0]
            conn.execute(
                f"UPDATE run_entity SET previous_run_id={previous_id if previous_id else 'NULL'} where id={run_id}"
            )
            previous_id = run_id


def downgrade():
    with op.batch_alter_table("run_entity") as batch_op:
        batch_op.drop_column("branch_name")
