"""add cpuinfo to test_result

Revision ID: 04fc7a4a1902
Revises: 0ebd0b83fae2
Create Date: 2020-11-25 15:36:28.128520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "04fc7a4a1902"
down_revision = "0ebd0b83fae2"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("test_result_entity", sa.Column("machine_info", sa.JSON()))


def downgrade():
    with op.batch_alter_table("test_result_entity") as batch_op:
        batch_op.drop_column("machine_info")
