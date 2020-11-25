"""rename hash column

Revision ID: 0ebd0b83fae2
Revises: 989d5eee48f8
Create Date: 2020-11-25 10:51:26.227083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0ebd0b83fae2"
down_revision = "989d5eee48f8"
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("file_entity", "md5_hash", new_column_name="hash")


def downgrade():
    op.alter_column("file_entity", "hash", new_column_name="md5_hash")
