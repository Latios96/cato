"""run_batch_add_created_at_column

Revision ID: 7a69c3f1d789
Revises: 6332525ea212
Create Date: 2022-09-27 10:29:01.828842

"""

import datetime

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "7a69c3f1d789"
down_revision = "6332525ea212"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("run_batch_entity", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("created_at", sa.DateTime, nullable=True),
        )

    conn = op.get_bind()
    run_batches = conn.execute(
        "select id from run_batch_entity order by id asc"
    ).fetchall()
    for run_batch in run_batches:
        run_batch_id = run_batch[0]
        conn.execute(
            f"UPDATE run_batch_entity SET created_at='{datetime.datetime.now() + datetime.timedelta(seconds=run_batch_id)}'"
        )

    with op.batch_alter_table("run_batch_entity", schema=None) as batch_op:
        batch_op.alter_column("created_at", existing_type=sa.DateTime, nullable=False)


def downgrade():
    with op.batch_alter_table("run_batch_entity") as batch_op:
        batch_op.drop_column("created_at")
