"""add image size

Revision ID: d57a90012ac1
Revises: b4117526e49a
Create Date: 2020-12-21 13:16:02.049768

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.

revision = "d57a90012ac1"
down_revision = "b4117526e49a"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("image_entity", sa.Column("width", sa.Integer()))
    op.add_column("image_entity", sa.Column("height", sa.Integer()))


def downgrade():
    with op.batch_alter_table("image_entity") as batch_op:
        batch_op.drop_column("width")
        batch_op.drop_column("height")
