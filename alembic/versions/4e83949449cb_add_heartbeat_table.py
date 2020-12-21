"""add heartbeat table

Revision ID: 4e83949449cb
Revises: d57a90012ac1
Create Date: 2020-12-21 15:56:44.982217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4e83949449cb"
down_revision = "d57a90012ac1"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "test_heartbeart_entity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column(
            "test_result_entity_id",
            sa.INTEGER,
            sa.ForeignKey("test_result_entity.id"),
            unique=True,
        ),
        sa.Column("last_beat", sa.DateTime(), nullable=False),
    )


def downgrade():
    op.drop_table("test_heartbeart_entity")
