"""file add byte_count

Revision ID: d91f2017c6a8
Revises: 2c52308bea0e
Create Date: 2025-10-05 15:45:57.724086

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "d91f2017c6a8"
down_revision = "2c52308bea0e"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("file_entity", sa.Column("byte_count", sa.BigInteger()))


def downgrade():
    with op.batch_alter_table("file_entity") as batch_op:
        batch_op.drop_column("byte_count")
