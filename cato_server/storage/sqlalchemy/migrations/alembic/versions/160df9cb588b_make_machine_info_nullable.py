"""make machine info nullable

Revision ID: 160df9cb588b
Revises: b9c29616b40e
Create Date: 2021-04-24 15:22:27.106562

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "160df9cb588b"
down_revision = "b9c29616b40e"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("test_result_entity") as batch_op:
        batch_op.alter_column("machine_info", existing_type=sa.JSON, nullable=True)


def downgrade():
    with op.batch_alter_table("test_result_entity") as batch_op:
        batch_op.alter_column("machine_info", existing_type=sa.JSON, nullable=False)
