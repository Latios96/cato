"""rename hash column

Revision ID: 0ebd0b83fae2
Revises: 989d5eee48f8
Create Date: 2020-11-25 10:51:26.227083

"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "0ebd0b83fae2"
down_revision = "989d5eee48f8"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("file_entity") as batch_op:
        batch_op.alter_column("md5_hash", new_column_name="hash")


def downgrade():
    with op.batch_alter_table("file_entity") as batch_op:
        batch_op.alter_column("hash", new_column_name="md5_hash")
