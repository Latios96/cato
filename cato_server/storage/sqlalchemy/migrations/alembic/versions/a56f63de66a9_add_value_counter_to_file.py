"""add value counter to file

Revision ID: a56f63de66a9
Revises: 237a9afdebce
Create Date: 2020-12-11 19:53:42.813438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a56f63de66a9"
down_revision = "237a9afdebce"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("file_entity", sa.Column("value_counter", sa.Integer()))


def downgrade():
    with op.batch_alter_table("file_entity") as batch_op:
        batch_op.drop_column("value_counter")
