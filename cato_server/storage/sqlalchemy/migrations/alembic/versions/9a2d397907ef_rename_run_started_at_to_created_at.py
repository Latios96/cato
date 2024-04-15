"""rename run started at to created at

Revision ID: 9a2d397907ef
Revises: 7a69c3f1d789
Create Date: 2022-11-06 12:36:43.582992

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "9a2d397907ef"
down_revision = "7a69c3f1d789"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("run_entity") as batch_op:
        batch_op.alter_column("started_at", new_column_name="created_at")


def downgrade():
    with op.batch_alter_table("run_entity") as batch_op:
        batch_op.alter_column("created_at", new_column_name="started_at")
