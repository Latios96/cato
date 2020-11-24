"""create file_entity table

Revision ID: 989d5eee48f8
Revises: 20aef8e365cf
Create Date: 2020-11-25 00:16:32.870125

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '989d5eee48f8'
down_revision = '20aef8e365cf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "file_entity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("md5_hash", sa.String(), nullable=False),
    )


def downgrade():
    op.drop_table('file_entity')

