"""create run table

Revision ID: 61785bfb06f9
Revises: a1dd8935f10d
Create Date: 2020-11-24 16:57:26.501464

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "61785bfb06f9"
down_revision = "a1dd8935f10d"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "run_entity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("project_entity_id", sa.Integer, sa.ForeignKey("project_entity.id")),
        sa.Column("started_at", sa.DateTime),
    )


def downgrade():
    op.drop_table("run_entity")
