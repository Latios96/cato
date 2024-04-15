"""make test results seconds optional

Revision ID: 3e4601a725e1
Revises: da4efe7d8eb4
Create Date: 2021-08-05 10:18:11.639507

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3e4601a725e1"
down_revision = "da4efe7d8eb4"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("test_result_entity") as batch_op:
        batch_op.alter_column("seconds", existing_type=sa.FLOAT(), nullable=True)


def downgrade():
    with op.batch_alter_table("test_result_entity") as batch_op:
        batch_op.alter_column("seconds", existing_type=sa.FLOAT(), nullable=False)
