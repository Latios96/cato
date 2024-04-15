"""create project table

Revision ID: a1dd8935f10d
Revises: 
Create Date: 2020-11-24 16:54:32.884344

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "a1dd8935f10d"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "project_entity",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(), nullable=False, unique=True),
    )


def downgrade():
    op.drop_table("project_entity")
